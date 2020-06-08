import contextlib


class PartialProxy:
    def __init__(self, proxied_object):
        super().__init__()
        super().__setattr__("_proxy_active", False)
        super().__setattr__("proxied_object", proxied_object)

    @contextlib.contextmanager
    def pause_proxy(self):
        self.proxy_stop()
        try:
            yield None
        finally:
            self.proxy_start()

    def proxy_start(self):
        self._proxy_active = True

    def proxy_stop(self):
        self._proxy_active = False

    def _hasattribute(self, name):
        try:
            self.__getattribute__(name)
        except AttributeError:
            return False
        return True

    def __setattr__(self, name, value):
        # Pass through all things not explicitely defined
        if self._hasattribute(name) or not self._proxy_active:
            super().__setattr__(name, value)
        else:
            setattr(self.proxied_object, name, value)

    def __getattr__(self, name):
        # Pass through all things not explicitely defined
        return getattr(self.proxied_object, name)

    def __getitem__(self, *args, **kwargs):
        return self.proxied_object.__getitem__(*args, **kwargs)

    def __setitem__(self, *args, **kwargs):
        return self.proxied_object.__setitem__(*args, **kwargs)

    def __repr__(self):
        return f"Proxy<{str(self.proxied_object)}>"
