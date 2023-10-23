import argparse
import logging
import os
import time
import datetime
from typing import Union
from zipfile import ZipFile, ZIP_DEFLATED
from rarfile import RarFile

OMNIBUS = "omnibus"
COMIC_RAR = ".cbr"
COMIC_ZIP = ".cbz"

def main(comics_path: str, compression=ZIP_DEFLATED):
  logging.debug("comics_path %s", comics_path)
  omnibus_name = os.path.basename(os.path.normpath(comics_path)) + ".cbz"
  logging.debug("omnibus_name %s", omnibus_name)
  omnibus_directory = os.path.join(comics_path, OMNIBUS)
  logging.debug("omnibus_directory %s", omnibus_directory)
  omnibus_path = os.path.join(omnibus_directory, omnibus_name)
  logging.debug("omnibus_path %s", omnibus_path)
  if not os.path.exists(omnibus_path):
    logging.info("Creating new omnibus %s", omnibus_name)
    os.makedirs(omnibus_directory)
  else:
    logging.info("Recreating existing omnibus %s", omnibus_name)
  omnibus_images = 0
  total_comics = 0
  with ZipFile(omnibus_path, "w", compression) as omnibus_archive:
    for root, dirs, files in os.walk(os.path.abspath(comics_path)):
      logging.debug("root %s", root)
      logging.debug("dirs %s", dirs)
      logging.debug("files %s", files)
      if root == omnibus_directory:
        logging.debug("Skipping omnibus directory %s", omnibus_directory)
        continue
      logging.info("Processing comics directory %s", root)
      for file in sorted(files):
        logging.debug("file %s", file)
        file_name, ext = os.path.splitext(file)
        logging.debug("ext %s", ext)
        file_path = os.path.join(root, file)
        logging.debug("file_path %s", file_path)
        try:
          if ext == COMIC_RAR:
            comic_archive = RarFile(file_path)
          elif ext == COMIC_ZIP:
            comic_archive = ZipFile(file_path)
          else:
            logging.debug("Skipping unknown extension %s", ext)
            continue
          with comic_archive:
            logging.info("Processing comic %s", file)
            omnibus_images += process_comic(comic_archive, omnibus_archive)
            logging.debug("omnibus_images %s", omnibus_images)
            logging.info("Finished processing comic")
            total_comics += 1
            logging.debug("total_comics %s", total_comics)
        except Exception as ex:
          logging.error("An error occured while processing %s", file)
          logging.error(str(ex))
      logging.info("Finished processing directory")
  logging.info("Total comics processed %s", total_comics)
  logging.info("Total images processed %s", omnibus_images)
  total_size = os.path.getsize(omnibus_path)
  logging.debug("total_size %s", total_size)
  logging.info("Total omnibus size %s", total_size)

def process_comic(comic: Union[ZipFile, RarFile], omnibus: ZipFile) -> int:
  """Copy images from comic archive to omnibus archive. Returns number of images copied."""
  file_base = os.path.splitext(os.path.basename(comic.filename))[0]
  logging.debug("file_base %s", file_base)
  images = sorted(comic.namelist())[1:-1]
  total_images = len(images)
  logging.debug("total_images")
  logging.info("Comic contains %s images", total_images)
  for index, image in enumerate(images):
    logging.debug("index %s", index)
    logging.debug("image %s", image)
    extension = os.path.splitext(image)[1]
    logging.debug("extension %s", extension)
    file_name = f"{file_base} {index+1:03d}{extension}"
    logging.debug("file_name %s", file_name)
    data = comic.read(image)
    omnibus.writestr(file_name, data)
  return total_images

def setup_logger(path, persist=False, debug=False):
  file_name = datetime.datetime.utcnow().isoformat() + ".txt"
  logging.basicConfig(
    filename=os.path.join(path, OMNIBUS, file_name) if persist else None,
    level=logging.DEBUG if debug else logging.INFO,
    format="%(asctime)s | %(levelname)-8s | %(message)s",
  )

def directory(value: str) -> str:
  if not os.path.exists(value):
    raise argparse.ArgumentTypeError("does not exist")
  if not os.path.isdir(value):
    raise argparse.ArgumentTypeError("not a directory")
  return os.path.abspath(value)

def setup_parser():
  parser = argparse.ArgumentParser(description="Create omnibus archive from directory of individual issues.")
  parser.add_argument("path", type=directory, help="path to directory of issues")
  parser.add_argument("-p", "--persist", action="store_true", help="persist logs to disk")
  parser.add_argument("-d", "--debug", action="store_true", help="show debug logs")
  return parser.parse_args()

if __name__ == "__main__":
  args = setup_parser()
  setup_logger(args.path, args.persist, args.debug)
  start_time = time.time()
  logging.info("Running omnibus script")
  main(args.path)
  end_time = time.time()
  total_time = end_time - start_time
  logging.info("Total time %s", total_time)
  logging.info("Finished running omnibus script")