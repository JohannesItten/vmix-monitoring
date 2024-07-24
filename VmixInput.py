class VmixInput:
    def __init__(self, number: int, 
    key: str, title: str, overlays: list, props: dict, is_active: bool):
        self.number = number
        self.key = key
        self.title = title
        self.overlays = overlays
        self.props = props
        self.is_active = is_active


    #if same key(guid) means same input
    def __eq__(self, other):
        if not isinstance(other, (str, input)):
            False
        return self.key == key 


    #to make sortable by input number
    def __lt__(self, other):
        if not isinstance(other, input):
            raise TypeError("Right op must be instance of VmixInput")
        return self.number < other.number


    def __str__(self):
        return self.number + ": " + self.title


    def get_prop(self, prop):
        if not prop in self.props: return -1
        return self.props[prop]