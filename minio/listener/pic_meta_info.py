import exifread
import sys
# Open image file for reading (binary mode)
def get_exif_data(ifile):
    # Return Exif tags
    try:
        with open(ifile,'rb') as f:
            f = open(sys.argv[1], 'rb')
            tags = exifread.process_file(f)
            tags_dict = {}
            # Print all tags
            for tag in tags.keys():
                if tag not in ('JPEGThumbnail', 'TIFFThumbnail', 'Filename',
                            'EXIF MakerNote'):
                    tags_dict[f'{tag}'] = f"{{tags[tag]}}"
            return tags_dict

        # Close file
        f.close()
    except Exception as e:
        print (f"failure {e}")
        return {'_tags_error': f'{e}'}
