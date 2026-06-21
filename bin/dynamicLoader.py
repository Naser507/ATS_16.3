import sys
import os
import importlib.util
import wx

class DynamicLoader:
    def __init__(self):
        self.root = os.path.dirname(os.path.abspath(__file__))
        self.paths = [
            self.root,
            os.path.join(self.root, 'src'),
            os.path.join(self.root, 'Shared_Lib'),
            os.path.join(self.root, 'Engine')
        ]
        for path in self.paths:
            if path not in sys.path:
                sys.path.insert(0, path)
        self.extensions = ['.py', '.pyd', '.so', '.dll']
        self.cache = {}

    def load(self, module_name):
        # Return from cache if already loaded
        if module_name in self.cache:
            return self.cache[module_name]

        for path in self.paths:
            for ext in self.extensions:
                file_path = os.path.join(path, f"{module_name}{ext}")

                if os.path.exists(file_path):
                    spec = importlib.util.spec_from_file_location(module_name, file_path)

                    if spec and spec.loader:
                        module = importlib.util.module_from_spec(spec)
                        spec.loader.exec_module(module)

                        # Cache the module
                        self.cache[module_name] = module
                        return module
                    else:
                        continue

        # Error handling (no duplicate wx.App creation)
        if wx.GetApp():
            wx.MessageBox(f"Module not found: {module_name}", "Error", wx.OK | wx.ICON_ERROR)
        else:
            print(f"Module not found: {module_name}")

        return None


loader = DynamicLoader()