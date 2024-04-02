import os
from textx import language, metamodel_from_file, get_model, get_metamodel

__version__ = "0.1.0.dev"

def state_id_definer_scope(state_id, attr, attr_ref):
    """
    Look up the state def. if the state doesnt already exist, create a new state
    """
    m = get_model(state_id)  # get the model of the currently processed element
    name = attr_ref.obj_name  # the name of currently looked up element

    for s in m.states:
        if s.state_id is None:
            continue
        if s.state_id.name != name:
            continue
        return s.state_id
    
    mm = get_metamodel(m)  # else, create it and store it in the model
    state_id = mm["StateID"]()
    state_id.name = name
    return state_id

def next_state_definer_scope(state_id, attr, attr_ref):
    m = get_model(state_id)  # get the model of the currently processed element
    name = attr_ref.obj_name  # the name of currently looked up element

    
    for s in m.states:
        if s.state_id is None:
            continue
        if s.state_id.name != name:
            continue
        return s.state_id
    
    # state must be halt at this point
    for s in m.states:
        if s.next_state is None:
            continue
        if s.next_state.name != name:
            continue
        return s.next_state
    
    # create a new halt state id if halt does not already exist
    mm = get_metamodel(m)  # else, create it and store it in the model
    state_id = mm["StateID"]()
    state_id.name = name
    return state_id

@language('tml', '*.tm')
def tml_language():
    "tml language"
    current_dir = os.path.dirname(__file__)
    mm = metamodel_from_file(os.path.join(current_dir, 'tml.tx'))

    # Here if necessary register object processors or scope providers
    # http://textx.github.io/textX/stable/metamodel/#object-processors
    # http://textx.github.io/textX/stable/scoping/
    mm.register_scope_providers(
        {
            "State.state_id": state_id_definer_scope,
            "State.next_state": next_state_definer_scope,
        }
    )

    return mm
