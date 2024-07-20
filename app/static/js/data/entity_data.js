export const entity_json = `{
    "stick": {
        "display": "Stick",
        "value": 1,
        "weight": 3,
        "is_obtainable": true
    },
    "vine": {
        "display": "Vine",
        "value": 4,
        "weight": 1,
        "is_obtainable": true
    },
    "stone": {
        "display": "Stone",
        "value": 2,
        "weight": 5,
        "is_obtainable": true
    },
    "rope": {
        "display": "Rope",
        "value": 15,
        "weight": 3,
        "is_obtainable": true,
        "is_craftable": true,
        "cost": [
            {
				"id": "vine",
                "qty": 3
            }
        ],
		"description": "A simple rope made from braided vines."
	},
	"basket": {
		"display": "Basket",
		"is_obtainable": true,
		"is_craftable": true,
		"is_equippable": true,
		"cost": [
			{
				"id": "vine",
                "qty": 1
			},
			{
				"id": "stick",
                "qty": 10
			}
		],
		"description": "Allows you to carry more items when foraging.",
		"max_quantity": 1
	}
}`