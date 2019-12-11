import requests
import enum


API_URL_SECURITY_WAIT_TIMES = "https://avi-prod-mpp-webapp-api.azurewebsites.net/api/v1/SecurityWaitTimesPoints/{airport}"


class SecurityQueueType(enum.Enum):
    MAIN = 0
    TSA_PRECHECK = 1

    @classmethod
    def from_string(cls, string) -> "SecurityQueueType":
        if string == "Reg":
            return cls.MAIN
        elif string == "TSAPre":
            return cls.TSA_PRECHECK
        else:
            raise ValueError("Invalid queue type: {}".format(string))


class SecurityWaitTimeEntry:
    def __init__(self, terminal, check_point, queue_type, wait_time_seconds):
        self.terminal = terminal
        self.check_point = check_point
        self.queue_type = queue_type
        self.wait_time_seconds = wait_time_seconds


def collect_security_wait_times(airport) -> [SecurityWaitTimeEntry]:
    session = requests.Session()
    session.headers.update({"referer": "https://www.jfkairport.com"})

    wait_times = session.get(API_URL_SECURITY_WAIT_TIMES.format(airport=airport)).json()
    results = []

    for entry in wait_times:
        results.append(
            SecurityWaitTimeEntry(
                entry["terminal"],
                entry["checkPoint"],
                SecurityQueueType.from_string(entry["queueType"]),
                int(entry["timeInSeconds"]),
            )
        )

    return results
