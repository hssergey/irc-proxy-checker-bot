import settings
import irc.bot
from irc.bot import ServerSpec
from proxy_checker import check_bad_host, load_tor_ips
from vkhoroscope import vkhoroscope



class ProxyCheckerBot(irc.bot.SingleServerIRCBot):
    nick = None
    
    def __init__(self, server, port, username, password, nick):
        self.nick = nick
        server_spec = ServerSpec(server, port, password)
        irc.bot.SingleServerIRCBot.__init__(self, [server_spec], nick, username, username = username)


    def irc_print(self, ch, message):
        lines = message.split("\n")
        for line in lines:
            line = line.strip()
            if line:
                self.connection.privmsg(ch, line)
            
 
    def on_pubmsg(self, c, e):
#         print("%s: %s" % (c, e))
        ch = e.target
        message = e.arguments[0]
#         print(message)
        if "вкгороскоп" in message:
            self.irc_print(ch, vkhoroscope(message))
        

    def on_join(self, connection, event):
        ch = event.target
        nick = event.source.nick
        print("on_join: %s : %s : %s" % (ch, event.source, event.source.host))
        if nick == self.nick:
            return
        result = check_bad_host(event.source.host)
        if result[0]:
            line = "!!! %s: %s " % (event.source.host, result[1])
            print(line)
#             self.connection.privmsg(ch, line)
            self.connection.notice(self.nick, line)
            self.connection.mode(ch, "+B *!*@%s" % event.source.host)
            self.connection.kick(ch, nick, "malicious host detected")
        

    def on_privmsg(self, c, e):
        self.do_command(e, e.arguments[0])
        
   
    def do_command(self, e, cmd):
#         print("got cmd: %s" % cmd)
        nick = e.source.nick
        if not nick == settings.admin_nick:
            return
        c = self.connection
        cmds = cmd.strip().split(" ")

        if cmds[0] == "disconnect":
            self.disconnect()
        elif cmds[0] == "die":
            self.die()
        elif cmds[0] == "join":
            if len(cmds) == 2:
                c.notice(nick, "joining %s" % cmds[1])
                c.join(cmds[1])
#         else:
#             c.notice(nick, "Not understood: " + cmd)
            
    

load_tor_ips()
bot = ProxyCheckerBot(settings.server, settings.port, settings.username, settings.password, settings.nick)
bot.start()


    