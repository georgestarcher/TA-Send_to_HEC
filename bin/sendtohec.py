
# encoding = utf-8
# Always put this line at the beginning of this file
import ta_send_to_hec_declare 

import os
import sys

from alert_actions_base import ModularAlertBase 
import modalert_sendtohec_helper

class AlertActionWorkersendtohec(ModularAlertBase):

    def __init__(self, ta_name, alert_name):
        super(AlertActionWorkersendtohec, self).__init__(ta_name, alert_name)

    def validate_params(self):

        if not self.get_param("u_splunkserver"):
            self.log_error('u_splunkserver is a mandatory parameter, but its value is None.')
            return False

        if not self.get_param("u_splunkserverport"):
            self.log_error('u_splunkserverport is a mandatory parameter, but its value is None.')
            return False

        if not self.get_param("u_hectoken"):
            self.log_error('u_hectoken is a mandatory parameter, but its value is None.')
            return False

        if not self.get_param("u_senddatatype"):
            self.log_error('u_senddatatype is a mandatory parameter, but its value is None.')
            return False
        return True

    def process_event(self, *args, **kwargs):
        status = 0
        try:
            self.prepare_meta_for_cam()

            if not self.validate_params():
                return 3 
            status = modalert_sendtohec_helper.process_event(self, *args, **kwargs)
        except (AttributeError, TypeError) as ae:
            self.log_error("Error: {}. Please double check spelling and also verify that a compatible version of Splunk_SA_CIM is installed.".format(ae.message))
            return 4
        except Exception as e:
            msg = "Unexpected error: {}."
            if e.message:
                self.log_error(msg.format(e.message))
            else:
                import traceback
                self.log_error(msg.format(traceback.format_exc()))
            return 5
        return status

if __name__ == "__main__":
    exitcode = AlertActionWorkersendtohec("TA-Send_to_HEC", "sendtohec").run(sys.argv)
    sys.exit(exitcode)
