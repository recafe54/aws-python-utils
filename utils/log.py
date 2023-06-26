class Logger(object):
    def __init__(self):
        self.WANNING = '\033[93m'
        self.FAIL = '\033[91m'
        self.ENDC = '\033[0m'    
        self.INFO = '\033[92m'
        self.OKGREEN = '\033[94m'
        self.BOLD = '\033[1m'
        self.UNDERLINE = '\033[4m'
        self.HEADER = '\033[95m'
        self.OKBLUE = '\033[94m'
        
    def info(self, message):
        sys.stdout.write(self.INFO + ' ' + message + self.ENDC + '\n')
        
    def ok(self, message):
        sys.stdout.write(self.OKGREEN + ' ' + message + self.ENDC + '\n')
        
    def fail(self, message):
        sys.stdout.write(self.FAIL + ' ' + message + self.ENDC + '\n')
        
    def warning(self, message):
        sys.stdout.write(self.WANNING + ' ' + message + self.ENDC + '\n')
        
    def bold(self, message):
        sys.stdout.write(self.BOLD + ' ' + message + self.ENDC + '\n')
        
    def underline(self, message):
        sys.stdout.write(self.UNDERLINE + ' ' + message + self.ENDC + '\n')
        
    def header(self, message):
        sys.stdout.write(self.HEADER + ' ' + message + self.ENDC + '\n')
        
    def okblue(self, message):
        sys.stdout.write(self.OKBLUE + ' ' + message + self.ENDC + '\n')
        
    def write(self, message):
        sys.stdout.write(message + '\n')