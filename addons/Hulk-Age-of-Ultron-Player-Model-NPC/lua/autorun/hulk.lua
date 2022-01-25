player_manager.AddValidModel( "Hulk", "models/hopwire/marvel/hulkPM.mdl" );

local Category = "Marvel"

local NPC = { 	Name = "Hulk", 
				Class = "npc_citizen",
				Model = "models/hopwire/marvel/HulkNPC.mdl",
				Health = "40",
				KeyValues = { citizentype = 4 },
				Weapons = { "weapon_ar2", "weapon_smg1", "weapon_shotgun", "weapon_pistol" },
                                Category = Category    }

list.Set( "NPC", "npc_hulk_npc", NPC )