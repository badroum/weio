# import tornado
# import platform
# import subprocess
#
# from weioLib import weioConfig
# from handlers import loginHandler
#
# class WeioSigninHandler(loginHandler.BaseHandler):
#     def get(self):
#         try:
#             errormessage = self.get_argument("error")
#         except:
#             errormessage = ""
#         self.render("../www/signin.html", errormessage = errormessage)
#
#     def post(self):
#         confFile = weioConfig.getConfiguration()
#         fullName = self.get_argument("fullName", "")
#         passwd = self.get_argument("password", "")
#         login_required = self.get_argument("loginRequired", "NO")
#         boardname = self.get_argument("boardname", "")
#         timezone = self.get_argument("timezone", "UTC+1")
#         # This is two letters country code to be used to setup wifi region
#         countryCode = self.get_argument("countryCode", "")
#
#         print "************ ", fullName, passwd, boardname, countryCode
#
#         data = {}
#         # OK now is time to setup username and password
#         confFile['user'] = fullName
#         confFile['login_required'] = login_required
#         weioConfig.saveConfiguration(confFile)
#         confFile['timezone'] = timezone
#         output = "OK PASSWD"
#
#         #echo -e "weio\nweio" | passwd
#
#         # ATTENTION, DON'T MESS WITH THIS STUFF ON YOUR LOCAL COMPUTER
#         # First protection is mips detection, second is your own OS
#         # who hopefully needs sudo to change passwd on the local machine
#         if (platform.machine() == 'mips'):
#
#             # Change root password
#             command = "sh scripts/change_root_pswd.sh " + passwd
#             print "EXEC : " + command
#
#             try:
#                 subprocess.call(command, shell=True)
#                 firstTimeSwitch = "NO"
#                 confFile['first_time_run']=firstTimeSwitch
#             except:
#                 output = "ERR_CMD PASSWD"
#                 print output
#
#             # Change avahi name
#             command = "sh scripts/change_boardname.sh " + boardname
#             confFile['dns_name'] = boardname + ".local"
#             weioConfig.saveConfiguration(confFile)
#             print "EXEC : " + command
#
#             try:
#                 subprocess.call(command, shell=True)
#             except:
#                 output = "ERR_CMD BRDNAME"
#             # Change user time zone
#             if timezone:
#                 commandConfig = "uci set system.@system[0].timezone=" + timezone  # Set timezone on openwrt config (required for system reboot)
#                 commandCommitConfig = "uci commit system.@system[0].timezone"
#                 try:
#                     subprocess.call(commandConfig, shell=True)
#                     subprocess.call(commandCommitConfig, shell=True)
#                 except:
#                     output = "ERR_CMD TIMEZONE"
#         else:
#             # On PC
#             firstTimeSwitch = "NO"
#             confFile['first_time_run']=firstTimeSwitch
#
#         # Save new password in the config file
#         confFile['password'] = passwd
#
#         # Write in config file
#         weioConfig.saveConfiguration(confFile)
#
#         self.set_secure_cookie("user", tornado.escape.json_encode("weio"))
#         self.redirect(self.get_argument("next", u"/"))
