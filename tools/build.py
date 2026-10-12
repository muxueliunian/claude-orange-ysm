"""Build this standalone YSM project with Python 3.10+, standard library only.

Validation compares actual JSON fields and archive bytes; no hashes are computed.
"""
import json
from pathlib import Path
import struct
import zipfile

ROOT = Path(__file__).resolve().parents[1]
MODEL = ROOT / 'claude_orange'
OUT = ROOT / 'dist'


def strings(value):
    if isinstance(value, str):
        yield value
    elif isinstance(value, dict):
        for v in value.values():
            yield from strings(v)
    elif isinstance(value, list):
        for v in value:
            yield from strings(v)


def main():
    files = sorted(p for p in MODEL.rglob('*') if p.is_file())
    allowed = {'animations', 'avatar', 'controller', 'models', 'sounds', 'textures'}
    for path in files:
        relative = path.relative_to(MODEL)
        assert path.resolve().is_relative_to(MODEL.resolve()), relative
        assert relative.as_posix() == 'ysm.json' or relative.parts[0] in allowed, relative
        assert path.suffix.lower() in ('.json', '.png', '.ogg'), relative
        if path.suffix == '.json':
            json.loads(path.read_text(encoding='utf-8-sig'))
    manifest = json.loads((MODEL / 'ysm.json').read_text(encoding='utf-8-sig'))
    references = []
    for ref in strings(manifest):
        if ref.split('/')[0] in allowed:
            target = (MODEL / ref).resolve()
            assert target.is_relative_to(MODEL.resolve()) and target.is_file(), ref
            references.append(ref)
    geometry = json.loads((MODEL / 'models/main.json').read_text(encoding='utf-8'))['minecraft:geometry'][0]
    bones = {b['name']: b for b in geometry['bones']}
    assert len(bones) == len(geometry['bones'])
    for name, bone in bones.items():
        parent, chain = bone.get('parent'), {name}
        while parent:
            assert parent in bones and parent not in chain, name
            chain.add(parent)
            parent = bones[parent].get('parent')
    animations = json.loads((MODEL / 'animations/main.animation.json').read_text(encoding='utf-8'))['animations']
    assert manifest['properties']['preview_animation'] in animations
    assert 'idle' in animations and 'pre_parallel3' in animations
    png = (MODEL / 'textures/default.png').read_bytes()
    assert png[:8] == b'\x89PNG\r\n\x1a\n'
    texture_size = list(struct.unpack('>II', png[16:24]))
    OUT.mkdir(exist_ok=True)
    archive_path = OUT / 'claude_orange.zip'
    with zipfile.ZipFile(archive_path, 'w', compression=zipfile.ZIP_DEFLATED, compresslevel=6) as archive:
        for path in files:
            # Stable archive metadata; content is validated directly after writing.
            entry = zipfile.ZipInfo(path.relative_to(MODEL).as_posix(), (2026, 10, 13, 0, 0, 0))
            entry.compress_type = zipfile.ZIP_DEFLATED
            archive.writestr(entry, path.read_bytes())
    with zipfile.ZipFile(archive_path) as archive:
        assert 'ysm.json' in archive.namelist()
        assert len(archive.namelist()) == len(files)
        for path in files:
            assert archive.read(path.relative_to(MODEL).as_posix()) == path.read_bytes()
    report = {'files': len(files), 'manifest_references_checked': len(references),
              'bones': len(bones), 'cubes': sum(len(b.get('cubes', [])) for b in bones.values()),
              'main_animations': len(animations), 'texture_pixels': texture_size,
              'archive_bytes': archive_path.stat().st_size, 'archive_content_byte_comparison': 'pass',
              'file_inventory': [{'path': p.relative_to(MODEL).as_posix(), 'bytes': p.stat().st_size} for p in files]}
    (OUT / 'validation.json').write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8')
    print(json.dumps({k: v for k, v in report.items() if k != 'file_inventory'}, ensure_ascii=False))


if __name__ == '__main__':
    main()
