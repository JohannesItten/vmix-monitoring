import hashlib
import common.VmixState as VmixState

DEFAULT_PORT = '8088'


class Vmix:

    def __init__(self,
                 name,
                 unit,
                 ip,
                 port,
                 username=None,
                 password=None,
                 rule_name=None):
        self.name = name
        self.unit = unit
        self.ip = ip
        self.port = DEFAULT_PORT if port is None else port
        self.username = username
        self.password = password
        self.rule_name = rule_name
        self.state = None
        self.new_errors = []

        self.id = self.__get_vmix_id()
        self.api_uri = self.__get_vmix_api_uri()

    def __get_vmix_id(self):
        hash_template = '{}-{}-{}'.format(self.name, self.ip, self.unit)
        vmix_id = hashlib.md5(hash_template.encode('UTF-8'))
        return vmix_id.hexdigest()

    def __get_vmix_api_uri(self):
        if self.password is None or self.username is None:
            return 'http://{}:{}/api'.format(self.ip, self.port)
        url_template = 'http://{}:{}@{}:{}/api'
        return url_template.format(self.username,
                                   self.password,
                                   self.ip,
                                   self.port)

    def process_xml_snapshot(self, xml_snapshot, rules):
        if self.state is None:
            state = VmixState.VmixState(xml_snapshot=xml_snapshot, rules=rules)
            self.state = state
        previous_errors = self.state.errors.storage.copy()
        self.state.xml_snapshot = xml_snapshot
        self.state.update_state()
        self.__get_new_errors(previous_errors, self.state.errors.storage)

    def __get_new_errors(self, previous_errors, current_errors):
        if len(previous_errors) == 0:
            self.new_errors = list(current_errors.values())
            return
        prev_keys = set(previous_errors.keys())
        current_keys = set(current_errors.keys())
        new_errors_keys = prev_keys.symmetric_difference(current_keys)
        for key in new_errors_keys:
            if key in current_keys:
                self.new_errors.append(current_errors[key])
