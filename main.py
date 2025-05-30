import asyncio
import logging
from argparse import ArgumentParser
from aiopath import AsyncPath
from aioshutil import copy as async_copy

logging.basicConfig(level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')

async def copy_file(file: AsyncPath, output_dir: AsyncPath):
    try:
        ext = file.suffix[1:] if file.suffix else 'no_extension'
        target_dir = output_dir / ext

        if not await target_dir.exists():
            try:
                await target_dir.mkdir(parents=True)
            except FileExistsError:
                pass  

        await async_copy(file, target_dir / file.name)
    except Exception as e:
        logging.error(f"Помилка при копіюванні {file}: {e}")

async def read_folder(source_dir: AsyncPath, output_dir: AsyncPath):
    async for path in source_dir.glob("**/*"):
        if await path.is_file():
            await copy_file(path, output_dir)

def main():
    parser = ArgumentParser(description="Асинхронне сортування файлів за розширенням")
    parser.add_argument("source", type=str, help="Шлях до вихідної папки")
    parser.add_argument("output", type=str, help="Шлях до цільової папки")
    args = parser.parse_args()

    source_dir = AsyncPath(args.source)
    output_dir = AsyncPath(args.output)

    asyncio.run(read_folder(source_dir, output_dir))

if __name__ == "__main__":
    main()