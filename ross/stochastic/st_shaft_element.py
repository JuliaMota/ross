import numpy as np

from ross.shaft_element import ShaftElement

__all__ = ["ST_ShaftElement"]


class ST_ShaftElement:
    """Random shaft element.

    Creates an object containing a list with random instances of ShaftElement.

    Parameters
    ----------
    L : float, pint.Quantity, list
        Element length.
        Input a list to make it random.
    idl : float, pint.Quantity, list
        Inner diameter of the element at the left position.
        Input a list to make it random.
    odl : float, pint.Quantity, list
        Outer diameter of the element at the left position.
        Input a list to make it random.
    idr : float, pint.Quantity, list, optional
        Inner diameter of the element at the right position
        Default is equal to idl value (cylindrical element)
        Input a list to make it random.
    odr : float, pint.Quantity, list, optional
        Outer diameter of the element at the right position.
        Default is equal to odl value (cylindrical element)
        Input a list to make it random.
    material : ross.material, list of ross.material
        Shaft material.
        Input a list to make it random.
    n : int, optional
        Element number (coincident with it's first node).
        If not given, it will be set when the rotor is assembled
        according to the element's position in the list supplied to
    shear_effects : bool, optional
        Determine if shear effects are taken into account.
        Default is True.
    rotary_inertia : bool, optional
        Determine if rotary_inertia effects are taken into account.
        Default is True.
    gyroscopic : bool, optional
        Determine if gyroscopic effects are taken into account.
        Default is True.
    shear_method_calc : str, optional
        Determines which shear calculation method the user will adopt.
        Default is 'cowper'
    is_random : list
        List of the object attributes to become random.
        Possibilities:
            ["L", "idl", "odl", "idr", "odr", "material"]

    Attributes
    ----------
    elements : list
        display the list with random shaft elements.

    Example
    -------
    >>> import numpy as np
    >>> import ross.stochastic as srs
    >>> from ross.materials import steel
    >>> elms = srs.ST_ShaftElement(L=1,
    ...                            idl=0,
    ...                            odl=np.random.uniform(0.1, 0.2, 5),
    ...                            material=steel,
    ...                            is_random=["odl"],
    ...                            )
    >>> len(list(elms.__iter__()))
    5
    """

    def __init__(
        self,
        L,
        idl,
        odl,
        idr=None,
        odr=None,
        material=None,
        n=None,
        shear_effects=True,
        rotary_inertia=True,
        gyroscopic=True,
        shear_method_calc="cowper",
        is_random=None,
    ):

        if idr is None:
            idr = idl
            if "idl" in is_random and "idr" not in is_random:
                is_random.append("idr")
        if odr is None:
            odr = odl
            if "odl" in is_random and "odr" not in is_random:
                is_random.append("odr")

        attribute_dict = dict(
            L=L,
            idl=idl,
            odl=odl,
            idr=idr,
            odr=odr,
            material=material,
            n=n,
            axial_force=0,
            torque=0,
            shear_effects=shear_effects,
            rotary_inertia=rotary_inertia,
            gyroscopic=gyroscopic,
            shear_method_calc=shear_method_calc,
            tag=None,
        )
        self.is_random = is_random
        self.attribute_dict = attribute_dict

    def __iter__(self):
        """Return an iterator for the container.

        Returns
        -------
        An iterator over random shaft elements.
        """
        return iter(self.random_var(self.is_random, self.attribute_dict))

    def random_var(self, is_random, *args):
        """Generate a list of objects as random attributes.

        This function creates a list of objects with random values for selected
        attributes from ShaftElement.

        Parameters
        ----------
        is_random : list
            List of the object attributes to become stochastic.
        *args : dict
            Dictionary instanciating the ShaftElement class.
            The attributes that are supposed to be stochastic should be
            set as lists of random variables.

        Returns
        -------
        f_list : generator
            Generator of random objects.

        Example
        -------
        """
        args_dict = args[0]
        new_args = []
        for i in range(len(args_dict[is_random[0]])):
            arg = []
            for key, value in args_dict.items():
                if key in is_random:
                    arg.append(value[i])
                else:
                    arg.append(value)
            new_args.append(arg)
        f_list = (ShaftElement(*arg) for arg in new_args)

        return f_list
