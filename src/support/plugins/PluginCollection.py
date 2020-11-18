import inspect, sys, os, pkgutil
from support.plugins.NydusPlugin import NydusPlugin
from support.plugins.PluginListItem import PluginListItem
from support.Config import Config
from support.Logger import Logger

class PluginCollection(object):
    def __init__(self, worker):
        sys.path.append(os.path.dirname(sys.executable))
        self.reloadPlugins()
        worker.enterGame.connect(self.enterGame)
        worker.exitGame.connect(self.exitGame)
        worker.menuChanged.connect(self.menuChanged)
        worker.log.connect(lambda message: Logger().log(message))

    def enterGame(self, data, isReplay):
        for plugin in self.plugins:
            if Config().plugins[plugin.id]["enabled"]:
                try:
                    plugin.plugin.enterGame(data, isReplay)
                except Exception as e:
                    plugin.plugin.log("[" + plugin.id + "] Error in enterGame - " + str(e))

    def exitGame(self, data, isReplay):
        for plugin in self.plugins:
            if Config().plugins[plugin.id]["enabled"]:
                try:
                    plugin.plugin.exitGame(data, isReplay)
                except Exception as e:
                    plugin.plugin.log("[" + plugin.id + "] Error in exitGame: " + str(e))

    def menuChanged(self, data):
        for plugin in self.plugins:
            if Config().plugins[plugin.id]["enabled"]:
                try:
                    plugin.plugin.menuChanged(data)
                except Exception as e:
                    plugin.plugin.log("[" + plugin.id + "] Error in menuChanged: " + str(e))

    def reloadPlugins(self):
        Logger().log("[Plugins] Scanning for plugins")
        self.plugins = []
        self.seen_paths = []
        self.seen_plugins = []
        self.walkPackage("plugins")

    def walkPackage(self, package):
        config = Config()
        imported_package = __import__(package, fromlist=['blah'])
        
        # if there are dependencies, load them
        # note that this is probably bad 
        found = False
        package_dir = ""
        for path in imported_package.__path__:
            if os.path.isdir(path + "/packages"):
                package_dir = path + "/packages"
                Logger().log("[Plugins] Installing dependencies in " + package_dir)
                sys.path.insert(0, package_dir)
                break

        for _, pluginname, ispkg in pkgutil.iter_modules(imported_package.__path__, imported_package.__name__ + '.'):
            if not ispkg:
                try:
                    plugin_module = __import__(pluginname, fromlist=['blah'])
                    clsmembers = inspect.getmembers(plugin_module, inspect.isclass)
                    for (_, c) in clsmembers:
                        if issubclass(c, NydusPlugin) & (c is not NydusPlugin):
                            pluginName = c.__module__ + "." + c.__name__
                            if pluginName not in self.seen_plugins:
                                Logger().log("[Plugins] Found " + c.__name__ + " (" + pluginName + ")")
                                self.seen_plugins.append(pluginName)

                                # instantiate the plugin
                                plugin = c()
                                if pluginName not in config.plugins.keys():
                                    config.plugins[pluginName] = {
                                        'enabled': False,
                                        'showOnStartup': False
                                    }

                                if config.plugins[pluginName]['enabled']:
                                    if config.plugins[pluginName]['showOnStartup']:
                                        plugin.getUI()
                                    plugin.start()

                                self.plugins.append(PluginListItem(plugin, pluginName))
                                found = True
                except Exception as e:
                    Logger().log("[Plugins] PluginCollection error: " + str(e))
        
        # if we didnt find a plugin, remove the packages directory from the path
        if package_dir != "" and not found:
            print("removing " + package_dir)
            sys.path.remove(package_dir)

        all_current_paths = []
        if isinstance(imported_package.__path__, str):
            all_current_paths.append(imported_package.__path__)
        else:
            all_current_paths.extend([x for x in imported_package.__path__])

        for pkg_path in all_current_paths:
            if pkg_path not in self.seen_paths:
                self.seen_paths.append(pkg_path)
                child_pkgs = [p for p in os.listdir(pkg_path) if os.path.isdir(os.path.join(pkg_path, p))]
                for child_pkg in child_pkgs:
                    if child_pkg != 'packages':
                        self.walkPackage(package + '.' + child_pkg)