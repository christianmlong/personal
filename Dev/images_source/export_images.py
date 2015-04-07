# pylint: disable=C0111, W0142, R0903, R0922
import os
import socket
import subprocess
from itertools import product

PICKPACK_SCALING_FACTOR = 57
INLINE_IMAGE_HEIGHT = 40
BIG_CHECKMARK_IMAGE_HEIGHT = 200
SHOPFLOOR_MONITOR_EXAMPLE_IMAGE_HEIGHT = 24

CLIPPERSHIP_SCALING_FACTOR = 30
CLIPPERSHIP_SUFFIX = 'cs'

def main():
    """
    Main function
    """
    print "Start export"
    export_images()
    print "Export complete"

def export_images():
    """
    Starting with svg files, call Inkscape to generate .png bitmaps at a variety
    of sizes.
    """
    #export_common()
    #export_pickpack()
    export_shopfloor_monitor()

def export_common():
    metal_ion_image_names = ('ion',
                             'metal',
                            )
    other_image_names = ('un_2909',
                         'battery_doc1',
                         'battery_doc2',
                         'battery_doc3',
                         'battery_doc4',
                         'battery_doc5',
                         'battery_doc6',
                         'boxes',
                         'ormd',
                         'box_rating',
                         'dollar_sign',
                         'helmet',
                         'heavy_weight',
                        )
    custom_scaled = (('battery_doc7', 1.5),
                     ('red_x', 1.5),
                     ('p', .8),
                     ('grainger', .4),
                    )

    for image_name in metal_ion_image_names:
        export_both_metal_ion(image_name)
    for image_name in other_image_names:
        export_both_other(image_name)
    for export_info in custom_scaled:
        export_custom(*export_info)

def export_both_metal_ion(image_name):
    MetalIonImageExporter(image_name = image_name,
                          scaling_factor = PICKPACK_SCALING_FACTOR,
                         ).export_all()

    MetalIonImageExporter(image_name = image_name,
                          scaling_factor = CLIPPERSHIP_SCALING_FACTOR,
                          export_suffix = CLIPPERSHIP_SUFFIX,
                         ).export_all()

def export_both_other(image_name):
    OtherImageExporter(image_name = image_name,
                       scaling_factor = PICKPACK_SCALING_FACTOR,
                      ).export_all()

    OtherImageExporter(image_name = image_name,
                       scaling_factor = CLIPPERSHIP_SCALING_FACTOR,
                       export_suffix = CLIPPERSHIP_SUFFIX,
                      ).export_all()

def export_custom(image_name,
                  custom_scaling_factor,
                 ):
    OtherImageExporter(image_name = image_name,
                       scaling_factor = (PICKPACK_SCALING_FACTOR * custom_scaling_factor),
                      ).export_all()

    OtherImageExporter(image_name = image_name,
                       scaling_factor = (CLIPPERSHIP_SCALING_FACTOR * custom_scaling_factor),
                       export_suffix = CLIPPERSHIP_SUFFIX,
                      ).export_all()

def export_pickpack():
    # Images that are specific to Pick Pack. These are not exported for Clippership
    InlineImageExporter(image_height = INLINE_IMAGE_HEIGHT,
                       ).export_all()
    CheckmarkImageExporter(image_height = INLINE_IMAGE_HEIGHT,
                          ).export_all()
    BigCheckmarkImageExporter(image_height = BIG_CHECKMARK_IMAGE_HEIGHT,
                          ).export_all()

def export_shopfloor_monitor():
    # Images that are specific to the Shopfloor Monitor
    ShopfloorMonitorExampleImageExporter(image_height = SHOPFLOOR_MONITOR_EXAMPLE_IMAGE_HEIGHT,
                                        ).export_all()


class _ImageExporter(object):
    pass

class _WarningImageExporter(_ImageExporter):
    def __init__(self,
                 export_suffix=None,
                ):
        _ImageExporter.__init__(self)
        self.export_suffix = export_suffix

        # Calculate some paths
        hostname = socket.gethostname().lower()

        if hostname == 'dave3xp':
            base_path = r'D:\Documents\Christian\Documents\Work\IA\Miller\Local projects'
            self.inkscape_path = r"C:\Program Files\Inkscape\inkscape.exe"
            pick_pack_dir_name = 'PickPack'
        #elif hostname == '1bk2zq1-190':
        #    base_path = r'S:\Parts\Information Advantage\Projects'
        #    self.inkscape_path = r"C:\Program Files\Inkscape\inkscape.exe"
        elif hostname == 'hk5ggx1-190':
            base_path = r'C:\Information Advantage local files\Projects'
            self.inkscape_path = r"C:\Program Files (x86)\Inkscape\inkscape.exe"
            pick_pack_dir_name = 'Pick Pack'
        elif hostname == 'dave5':
            base_path = r'C:\Users\Christian Long\Documents\Documents\Work\Miller\Projects'
            self.inkscape_path = r"C:\Program Files (x86)\Inkscape\inkscape.exe"
            pick_pack_dir_name = 'Pick Pack'
        else:
            err_msg = "Unknown host %s" % hostname
            raise SystemError(err_msg)

        pickpack_wc = os.path.join(base_path,
                                   pick_pack_dir_name,
                                   'Dev',
                                   #'Prod Branch',
                                   'Working Copy',
                                  )

        self.source_path_base = os.path.join(pickpack_wc,
                                             'Dev',
                                             'images_source',
                                            )
        self.dest_path_base = os.path.join(pickpack_wc,
                                           'App',
                                           'Miller_Pickpack',
                                           'static',
                                           'img',
                                          )

    def export_all(self):
        raise NotImplementedError

    def call_inkscape(self,
                      source_path,
                      dest_path,
                      desired_height,
                     ):
        command_line = self._build_inkscape_command_line(
            source_path,
            dest_path,
            desired_height,
        )

        #print "Source %s" % source_path
        assert os.path.exists(source_path)
        #print "Dest path %s" % os.path.dirname(dest_path)
        assert os.path.exists(os.path.dirname(dest_path))

        #print command_line
        subprocess.call(command_line)

    def _build_inkscape_command_line(self,
                                    source_path,
                                    dest_path,
                                    desired_height,
                                   ):

        # On windows, this all gets converted to a string before being
        # passed to subprocess.call. Here I'm doing it explicitly.
        return (
            '"{}"'
            ' --file="{}"'
            ' --export-area-page'
            ' --export-png="{}"'
            ' --export-height={}'
        ).format(
            self.inkscape_path,
            source_path,
            dest_path,
            desired_height,
        )

    def _build_export_file_base_name(self,
                                     partial_name,
                                    ):
        if self.export_suffix is not None:
            return "%s_%s.png" % (partial_name,
                                  self.export_suffix,
                                 )
        else:
            return "%s.png" % partial_name


class _MultiSizeExporter(_WarningImageExporter):
    def __init__(self,
                 image_name,
                 scaling_factor,
                 export_suffix,
                ):
        _WarningImageExporter.__init__(self,
                                       export_suffix,
                                      )
        self.image_name = image_name
        self.scaling_factor = scaling_factor

    def build_export_info(self):
        raise NotImplementedError

    def export_all(self):
        for (file_base_name,
             size_text,
             desired_height,
            ) in self.build_export_info():
            source_path = os.path.join(self.source_path_base,
                                       "%s.svg" % file_base_name,
                                      )
            export_file_base_name = self._build_export_file_base_name(
                "%s_%s" % (file_base_name, size_text)
            )
            dest_path = os.path.join(self.dest_path_base,
                                     export_file_base_name,
                                    )
            self.call_inkscape(source_path,
                               dest_path,
                               desired_height,
                              )


class _OneSizeExporter(_WarningImageExporter):
    def __init__(self,
                 image_height,
                 export_suffix,
                ):
        _WarningImageExporter.__init__(self,
                                       export_suffix,
                                      )
        self.image_height = image_height

    def build_export_info(self):
        raise NotImplementedError

    def export_all(self,
                   additional_path_elements=None,
                  ):
        if additional_path_elements is None:
            additional_path_elements = []

        for file_base_name in self.build_export_info():
            source_path_elements = [self.source_path_base]
            source_path_elements.extend(additional_path_elements)
            source_path_elements.append("%s.svg" % file_base_name)
            source_path = os.path.join(*source_path_elements)
            export_file_base_name = self._build_export_file_base_name(
                file_base_name
            )
            dest_path_elements = [self.dest_path_base]
            dest_path_elements.extend(additional_path_elements)
            dest_path_elements.append(export_file_base_name)
            dest_path = os.path.join(*dest_path_elements)
            self.call_inkscape(source_path,
                               dest_path,
                               self.image_height,
                              )


class MetalIonImageExporter(_MultiSizeExporter):
    def __init__(self,
                 image_name,
                 scaling_factor,
                 export_suffix = None,
                ):
        _MultiSizeExporter.__init__(self,
                                    image_name,
                                    scaling_factor,
                                    export_suffix,
                                   )

    def build_export_info(self):

        base_names = (
        #    base name                      Index of the height value
            ("%s1" % self.image_name,     1),
            ("%s2" % self.image_name,     2),
        )

        variations = (
        #    file name      1 height    2 height
            ('large',       295,        430),
            ('medium',      192,        280),
            ('small',       124,        180),
        )

        temp_list = []

        for case in product(base_names, variations):
            file_base_name = case[0][0]
            size_text = case[1][0]
            raw_height = case[1][case[0][1]]
            desired_height = int((raw_height * self.scaling_factor) / 100)
            temp_list.append((file_base_name, size_text, desired_height))

        return temp_list


class OtherImageExporter(_MultiSizeExporter):
    def __init__(self,
                 image_name,
                 scaling_factor,
                 export_suffix = None,
                ):
        _MultiSizeExporter.__init__(self,
                                    image_name,
                                    scaling_factor,
                                    export_suffix,
                                   )

    def build_export_info(self):

        variations = (
        #    file name      export height
            ('large',       295),
            ('medium',      192),
            ('small',       124),
        )

        temp_list = []

        for variation in variations:
            size_text = variation[0]
            raw_height = variation[1]
            desired_height = int((raw_height * self.scaling_factor) / 100)
            temp_list.append((self.image_name, size_text, desired_height))

        return temp_list


class InlineImageExporter(_OneSizeExporter):
    def __init__(self,
                 image_height,
                 export_suffix = None,
                ):
        _OneSizeExporter.__init__(self,
                                  image_height,
                                  export_suffix,
                                 )

    def build_export_info(self):

        base = 'inline_'

        variations = (
            'm',
            'i',
            'mi',
            'blank',
            'th',
            'ormd',
        )

        return ['%s%s' % (base, variation) for variation in variations]


class CheckmarkImageExporter(_OneSizeExporter):
    def __init__(self,
                 image_height,
                 export_suffix = None,
                ):
        _OneSizeExporter.__init__(self,
                                  image_height,
                                  export_suffix,
                                 )

    def build_export_info(self):

        types = ('1', '2')

        colors = (
            'blank',
            'gray',
            'green',
            'red',
            'yellow',
        )

        return ['%s%s' % (color, type) for color in colors for type in types]


class BigCheckmarkImageExporter(_OneSizeExporter):
    def __init__(self,
                 image_height,
                 export_suffix = None,
                ):
        _OneSizeExporter.__init__(self,
                                  image_height,
                                  export_suffix,
                                 )

    def build_export_info(self):
        return ['green_large', ]


class ShopfloorMonitorExampleImageExporter(_OneSizeExporter):
    def __init__(self,
                 image_height,
                ):
        _OneSizeExporter.__init__(self,
                                  image_height,
                                  export_suffix=None,
                                 )
        self.additional_path_elements=['shopfloor_monitor']

    def export_all(self):
        _OneSizeExporter.export_all(self,
                                    additional_path_elements=self.additional_path_elements,
                                   )

    def build_export_info(self):

        base = '_key_'

        variations = (
            ('ts', 'solid'),
            ('ts', 'stripe'),
            ('ts', 'ghost'),
            ('ss', 'solid'),
            ('ss', 'stripe'),
            ('ss', 'ghost'),
            ('ss', 'dark'),
            ('s', 'solid'),
            ('s', 'stripe'),
            ('n', 'solid'),
            ('n', 'stripe'),
            ('n', 'ghost'),
            ('n', 'dark'),
        )

        return ['%s%s%s' % (variation[0], base, variation[1]) for variation in variations]










if __name__ == '__main__':
    main()


#call :export_inline
#
#goto:eof
#
#
#
#
#
#:export_inline
#set base_name=inline_
#set source_path_51=%source_path_base%\%base_name%m.svg
#set source_path_52=%source_path_base%\%base_name%i.svg
#set source_path_53=%source_path_base%\%base_name%mi.svg
#set source_path_54=%source_path_base%\%base_name%blank.svg
#set source_path_55=%source_path_base%\%base_name%th.svg
#set dest_path_51=%dest_path_base%\%base_name%m.png
#set dest_path_52=%dest_path_base%\%base_name%i.png
#set dest_path_53=%dest_path_base%\%base_name%mi.png
#set dest_path_54=%dest_path_base%\%base_name%blank.png
#set dest_path_55=%dest_path_base%\%base_name%th.png
#
#set inline_height=40
#
#%inkscape% ^
#--file="%source_path_51%" ^
#--export-area-page ^
#--export-png="%dest_path_51%" ^
#--export-height=%inline_height%
#
#%inkscape% ^
#--file="%source_path_52%" ^
#--export-area-page ^
#--export-png="%dest_path_52%" ^
#--export-height=%inline_height%
#
#%inkscape% ^
#--file="%source_path_53%" ^
#--export-area-page ^
#--export-png="%dest_path_53%" ^
#--export-height=%inline_height%
#
#%inkscape% ^
#--file="%source_path_54%" ^
#--export-area-page ^
#--export-png="%dest_path_54%" ^
#--export-height=%inline_height%
#
#%inkscape% ^
#--file="%source_path_55%" ^
#--export-area-page ^
#--export-png="%dest_path_55%" ^
#--export-height=%inline_height%
#
#goto:eof
