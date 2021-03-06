import os

from conans import ConanFile, Meson, tools


class GObjectIntrospectionConan(ConanFile):
    name = "gobject-introspection"
    version = tools.get_env("GIT_TAG", "1.59.3")
    description = ("Middleware layer between C libraries (using GObject) and language bindings")
    license = "GPL, LGPL"
    settings = "os", "arch", "compiler", "build_type"
    generators = "pkgconf"

    def build_requirements(self):
        self.build_requires("generators/1.0.0@camposs/stable")
        self.build_requires("meson/[>=0.51.2]")
        self.build_requires("pkgconf/1.6.3@camposs/stable")

    def requirements(self):
        self.requires("python/[>=3.8.2]@camposs/stable")
        self.requires("libffi/3.3@camposs/stable")
        self.requires("glib/2.62.0@camposs/stable")

    def source(self):
        tools.get("https://github.com/GNOME/gobject-introspection/archive/%s.tar.gz" % self.version)

    def build(self):
        args = ["--auto-features=disabled"]
        meson = Meson(self)
        meson.configure(source_folder="%s-%s" % (self.name, self.version), args=args, pkg_config_paths=os.environ["PKG_CONFIG_PATH"].split(":"))
        meson.install()

    def package_info(self):
        self.env_info.GI_TYPELIB_PATH.append(os.path.join(self.package_folder, "lib", "girepository-1.0"))
        self.env_info.PYTHONPATH = os.path.join(self.package_folder, "lib", "gobject-introspection")
