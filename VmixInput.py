class VmixInput:
    PROP_NOT_FOUND = -1

    def __init__(self, number: int, 
    key: str, title: str, overlays: list, texts: dict, props: dict):
        self.number = number
        self.key = key
        self.title = title
        self.overlays = overlays
        self.texts = texts
        self.props = props


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
        return f'Input {self.number}: {self.title}'


    def get_prop(self, prop):
        if not prop in self.props: return self.PROP_NOT_FOUND
        return self.props[prop]