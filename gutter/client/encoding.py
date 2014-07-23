from gutter.client.models import (
    Condition,
    Switch,
)
from gutter.client.regisry import (
    arguments,
    operators,
)
from gutter.client.iterfaces.interfaces_pb2 import (
    PBCondition,
    PBSwitch,
)

# XXX: Groos
STATES = vars(Switch.states)

class SwitchProtobufEncoding(object):

    @staticmethod
    def encode(switch):
        pbswitch = PBSwitch()

        pbswitch.name = switch.name
        pbswitch.label = switch.label
        pbswitch.compounded = switch.compounded
        pbswitch.concent = switch.concent

        pbswitch.state = PBSwitch.State.DESCRIPTOR.values_by_number[switch.state]

        for condition in switch.conditions:
            pbcondition = PBCondition()
            # pbcondition.argument =
            pbcondition.attribute = condition.attribute
            pbcondition.operator = condition.operator
            pbcondition.negative = condition.negative

            pbswitch.conditions.add(condition)

        return pbswitch.SerializeToString()

    @staticmethod
    def decode(data):
        pbswitch = PBSwitch.ParseFromString(data)
        switch = Switch(
            name=pbswitch.name,
            label=pbswitch.label,
            # XXX: This only works cause the numbers are synced. Should
            #      this change?
            state=pbswitch.state,
            concent=pbswitch.concent,
            compounded=pbswitch.compounded,
        )

        for pbcondition in pbswitch.conditions:
            condition = Condition(
                argument=arguments[pbcondition.argument],
                attribute=pbcondition.attribute,
                operator=operators[pbcondition.operator],
                negative=pbcondition.negative,
            )
            switch.conditions.append(condition)

        return switch
