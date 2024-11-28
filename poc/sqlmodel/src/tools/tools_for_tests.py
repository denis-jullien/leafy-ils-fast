import pydantic


def does_model_contain_submodel(model, submodel) -> list[bool, str]:
    """Check if a pydantic model contains another pydantic model
    planned to be used inside an assertion

    Parameters
    ----------
    model: pydantic model that should contain the submodel
    submodel

    Return
    ------
    boolean, message in case the assertion failed
    """
    result = all(
        model.model_dump().get(key, None) == val
        for key, val in submodel.model_dump().items()
    )
    failure_message = f"Model ({model}) fails to contain ({submodel})."
    return result, failure_message


def does_model_contain_submodel_updated(
    model, init_submodel, updated_submodel
) -> list[bool, str]:
    """Check if a pydantic model contains another pydantic model
    the init_submodel will be merged with all updated_submodel values that are not None
    planned to be used inside an assertion

    Parameters
    ----------
    model: pydantic model that should contain the submodel
    init_submodel
    updated_submodel

    Return
    ------
    boolean, message in case the assertion failed
    """
    submodel = init_submodel.model_dump()
    for key, value in updated_submodel.model_dump().items():
        if value is not None:
            submodel[key] = value

    result = all(
        model.model_dump().get(key, None) == val for key, val in submodel.items()
    )
    failure_message = f"Model ({model}) fails to contain ({submodel})."
    return result, failure_message
