from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS


class Geolocation:
    def get_exif(self, filename):
        image = Image.open(filename)
        image.verify()
        return image._getexif()

    def get_labeled_exif(self, exif):
        labeled = {}
        for (key, val) in exif.items():
            labeled[TAGS.get(key)] = val

        return labeled

    GPSInfo = {1: 'N', 2: ((36, 1), (7, 1), (5263, 100)), 3: 'W', 4: ((115, 1), (8, 1), (5789, 100)), 5: b'\x00', 6: (241175, 391), 7: ((19, 1), (8, 1), (40, 1)), 12: 'K', 13: (0, 1), 16: 'T', 17: (1017664, 4813), 23: 'T', 24: (1017664, 4813), 29: '2019:01:11', 31: (65, 1)}

    def get_geotagging(self, exif):
        if not exif:
            raise ValueError("No EXIF metadata found")

        geotagging = {}
        for (idx, tag) in TAGS.items():
            if tag == 'GPSInfo':
                if idx not in exif:
                    raise ValueError("No EXIF geotagging found")

                for (key, val) in GPSTAGS.items():
                    if key in exif[idx]:
                        geotagging[val] = exif[idx][key]

        return geotagging

    def get_decimal_from_dms(self, dms, ref):

        degrees = dms[0][0] / dms[0][1]
        minutes = dms[1][0] / dms[1][1] / 60.0
        seconds = dms[2][0] / dms[2][1] / 3600.0

        if ref in ['S', 'W']:
            degrees = -degrees
            minutes = -minutes
            seconds = -seconds

        return round(degrees + minutes + seconds, 5)

    def get_coordinates(self, geotags):
        lat = self.get_decimal_from_dms(geotags['GPSLatitude'], geotags['GPSLatitudeRef'])

        lon = self.get_decimal_from_dms(geotags['GPSLongitude'], geotags['GPSLongitudeRef'])
        string = [lat, lon]
        return string

    def run_program(self,image):
        exif = self.get_exif(image)
        geotags = self.get_geotagging(exif)
        return self.get_coordinates(geotags)



#print(g.run_program('image.jpg'))