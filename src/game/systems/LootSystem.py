import random

from ecs.system import System
from game.components import (
    InteractableComp,
    InventoryComp,
    ItemComp,
    LootRequestComp,
    LootTableComp,
    PositionComp,
    StackComp,
)
from ecs import World
class LootSystem(System):
    def __init__(self,seed:int|None=None,rng:random.Random|None=None):
        self.rng=rng or random.Random(seed)
    def tick(self,world:World,*args,**kwargs):
        #find all entity with LootRequestComp
        loot_request_entity=world.get_entities_with(LootRequestComp)
        for entity in loot_request_entity:
            loot_request:LootRequestComp|None=entity.get_component(LootRequestComp)#type:ignore
            if loot_request is None:
                continue
            source=world.get_entity(loot_request.source_entity_id)
            receiver=world.get_entity(loot_request.receiver_entity_id)
            context:str=loot_request.context
            if source is None or receiver is None:
                #invalid loot request comp
                entity.remove_component(LootRequestComp)
                continue
            #check is source has loottable and target has inventory
            loot_table:LootTableComp|None=source.get_component(LootTableComp)
            if loot_table is None:
                continue
            inventory=receiver.get_component(InventoryComp)
            if inventory is None:
                continue
            loot_table_data=self._merge_loot_table(loot_table,context)
            resolved_loot=self._roll_loot(loot_table_data)
            self._place_loot(world,inventory,source,resolved_loot)
            world.destroy_entity(source.id)
            world.destroy_entity(entity.id)

    @staticmethod
    def _merge_loot_table(
        loot_table:LootTableComp,
        context:str,
    )->dict[str,float]:
        """Merge common loot with specialized context overrides."""
        merged=dict(loot_table.common_loot)
        specialized=loot_table.specialized_loot.get(context)
        if specialized is not None:
            merged.update(specialized)
        return merged

    def _roll_loot(self,loot_table:dict[str,float])->dict[str,int]:
        """Roll item quantities from expected drop rates."""
        result={}
        for item_id,drop_rate in loot_table.items():
            guaranteed=int(drop_rate)
            fractional=drop_rate-guaranteed
            quantity=guaranteed
            if fractional > 0 and self.rng.random() < fractional:
                quantity+=1
            if quantity > 0:
                result[item_id]=quantity
        return result

    def _place_loot(
        self,
        world:World,
        inventory:InventoryComp,
        source,
        resolved_loot:dict[str,int],
    )->None:
        """Place loot into inventory and drop overflow on source position."""
        for item_id,quantity in resolved_loot.items():
            remaining=self._fill_existing_stacks(
                world,
                inventory,
                item_id,
                quantity,
            )
            remaining=self._create_inventory_stacks(
                world,
                inventory,
                item_id,
                remaining,
            )
            if remaining > 0:
                self._create_ground_loot(
                    world,
                    source,
                    item_id,
                    remaining,
                )

    def _fill_existing_stacks(
        self,
        world:World,
        inventory:InventoryComp,
        item_id:str,
        quantity:int,
    )->int:
        """Fill existing inventory stacks greedily."""
        remaining=quantity
        for item_entity_id in inventory.slots:
            if remaining <= 0 or item_entity_id is None:
                continue
            item_entity=world.get_entity(item_entity_id)
            if item_entity is None:
                continue
            item=item_entity.get_component(ItemComp)
            stack=item_entity.get_component(StackComp)
            if (
                item is None
                or stack is None
                or item.item_id != item_id
                or stack.quantity >= stack.max_quantity
            ):
                continue
            space=stack.max_quantity-stack.quantity
            added=min(space,remaining)
            stack.quantity+=added
            remaining-=added
        return remaining

    def _create_inventory_stacks(
        self,
        world:World,
        inventory:InventoryComp,
        item_id:str,
        quantity:int,
    )->int:
        """Create new item stack entities in empty inventory slots."""
        remaining=quantity
        weight,category,max_quantity=self._get_item_defaults(
            world,
            inventory,
            item_id,
        )
        for index,item_entity_id in enumerate(inventory.slots):
            if remaining <= 0:
                break
            if item_entity_id is not None:
                continue
            stack_quantity=min(max_quantity,remaining)
            item_entity=world.create_entity(name=item_id)
            item_entity.add_component(
                ItemComp(
                    item_id=item_id,
                    weight=weight,
                    category=category,
                )
            )
            item_entity.add_component(
                StackComp(
                    quantity=stack_quantity,
                    max_quantity=max_quantity,
                )
            )
            inventory.slots[index]=item_entity.id
            remaining-=stack_quantity
        return remaining

    def _create_ground_loot(
        self,
        world:World,
        source,
        item_id:str,
        quantity:int,
    )->None:
        """Create ground loot entities for inventory overflow."""
        weight,category,max_quantity=self._get_item_defaults(
            world,
            None,
            item_id,
        )
        source_position=source.get_component(PositionComp)
        remaining=quantity
        while remaining > 0:
            stack_quantity=min(max_quantity,remaining)
            loot_entity=world.create_entity(name=item_id)
            if source_position is not None:
                loot_entity.add_component(
                    PositionComp(
                        x=source_position.x,
                        y=source_position.y,
                    )
                )
            loot_entity.add_component(
                ItemComp(
                    item_id=item_id,
                    weight=weight,
                    category=category,
                )
            )
            loot_entity.add_component(
                StackComp(
                    quantity=stack_quantity,
                    max_quantity=max_quantity,
                )
            )
            loot_entity.add_component(
                InteractableComp(
                    actions={
                        "fetch":True,
                        "inspect":True,
                    }
                )
            )
            remaining-=stack_quantity

    @staticmethod
    def _get_item_defaults(
        world:World,
        inventory:InventoryComp|None,
        item_id:str,
    )->tuple[float,str,int]:
        """Return item defaults from existing stacks or fallback values."""
        if inventory is not None:
            for item_entity_id in inventory.slots:
                if item_entity_id is None:
                    continue
                item_entity=world.get_entity(item_entity_id)
                if item_entity is None:
                    continue
                item=item_entity.get_component(ItemComp)
                stack=item_entity.get_component(StackComp)
                if item is None or stack is None or item.item_id != item_id:
                    continue
                return item.weight,item.category,stack.max_quantity
        return 1.0,"material",50
