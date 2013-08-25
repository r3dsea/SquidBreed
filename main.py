import org.bukkit as bukkit
import org.bukkit.inventory.ItemStack as ItemStack
import org.bukkit.Material as Material
import org.bukkit.World as World
import org.bukkit.EntityEffect as EntityEffect
import org.bukkit.entity.Wolf as Wolf
import org.bukkit.entity.Squid as SSquid
import org.bukkit.scheduler.BukkitRunnable as BukkitRunnable
import org.bukkit.potion.PotionEffectType as Effect
import org.bukkit.potion.PotionEffect as PotionEffect

#----Error Codes----
#-Error 1: More then two squids are registered in the list. Probably lag based.
#-------------------

__plugin_name__ = "SquidBreed"
__plugin_version__ = "1.0"
prefix = "[%s]: "%__plugin_name__

def log(text):
    try:
	print(prefix + str(text))
    except:
	pass

class Runnable(BukkitRunnable):  
    def run(self):
	DistanceSquidsX = abs(int(rs[0].getLocation().getX()) - int(rs[1].getLocation().getX()))
	DistanceSquidsZ = abs(int(rs[0].getLocation().getZ()) - int(rs[1].getLocation().getZ()))
	if DistanceSquidsX <= 3 and DistanceSquidsZ <= 3: #Once squids are close enough, proceed
	    rs[0].getWorld().spawn(rs[0].getLocation(), SSquid)
	    del sd[:]
	    del rs[:]
	    self.cancel() #Ends timer/loop
	pass

@hook.enable
def onEnable():
	global chat_prefix #DarkBlue prefix
	global sd
	global rs
	
	sd = [] #Entity ID list for squid
	rs = [] #Actual entity list for squid
	chat_prefix = bukkit.ChatColor.DARK_BLUE ##Use with string modifiers
	log("SquidBreed v1.0 Enabled! Written by r3dsea.")

	@hook.disable
	def onDisable():
	    log("SquidBreed v1.0 Disabled.")

@hook.event("player.PlayerInteractEntityEvent", "normal")
def RightClickEntityEvent(event):
    EntityType = str(event.getRightClicked().getType())
    SquidClicked = event.getRightClicked()
    sd.append(event.getRightClicked().getEntityId())
    rs.append(event.getRightClicked())
    if EntityType == "SQUID":
	Player = event.getPlayer()
	ItemHeld = str(Player.getItemInHand().getType())
	if ItemHeld == "RAW_FISH":
	    NewWolf = SquidClicked.getWorld().spawn(SquidClicked.getLocation(), Wolf)
	    NewWolf.playEffect(EntityEffect.WOLF_HEARTS)
	    NewWolf.remove()
	    AmountHeld = int(Player.getItemInHand().getAmount())
	    if AmountHeld == 1:
		Player.setItemInHand(ItemStack(Material.AIR, 1, 1))
		if len(sd) == 2:
		    PlayerName = str(event.getPlayer().getName())
		    if sd[0] == sd[1]: #Same squids, try again
			sd.remove(sd[1]) #Removes recently second click from list.
			
		    elif len(sd) > 2:
			del sd[:]
			del rs[:]
			
		    else: #Different Squids, begin breeding process
			rs[0].setTarget(rs[1])
			rs[1].setTarget(rs[0])
			#----Targeting Debug-----------------
			#print rs[0].getTarget().getEntityId() 
			#print rs[1].getEntityId()
			#print rs[1].getTarget().getEntityId()
			#print rs[0].getEntityId()
			#-------------------------------------
			Runnable().runTaskTimer(pyplugin, 0, 20)
		    
	    else:
		Player.getItemInHand().setAmount(AmountHeld - 1)
		if len(sd) == 2:
		    PlayerName = str(event.getPlayer().getName())
		    if sd[0] == sd[1]: #Same squids, try again
			sd.remove(sd[1]) #Removes recently second click from list.
			
		    elif len(sd) > 2:
			del sd[:]
			del rs[:]
			
		    else: #Different Squids, begin breeding process
			rs[0].setTarget(rs[1])
			rs[1].setTarget(rs[0])
			#----Targeting Debug-----------------
			#print rs[0].getTarget().getEntityId() 
			#print rs[1].getEntityId()
			#print rs[1].getTarget().getEntityId()
			#print rs[0].getEntityId()
			#-------------------------------------
			Runnable().runTaskTimer(pyplugin, 0, 20)
	else:
	    del sd[:]
	    del rs[:]