.. _table:

Table
=====
The table directive with ansys sphinx theme allows for rendering of tables.
There are different types of tables, such as the data table, longtable-centered,
and table-centered, each serving different purposes.

Normal table
------------


.. table:: Truth table for "not"
   :widths: auto
   :align: center

   +--------------------+------------------------+----------------------------------+
   |     **A**          |    **B**               |       **C**                      |
   +====================+========================+==================================+
   |                    ||    True               ||         False                   |
   |        False       ||    False              ||         True                    |
   +--------------------+------------------------+----------------------------------+
   |                    ||    True               ||         False                   |
   |       False        ||    False              ||         True                    |
   +--------------------+------------------------+----------------------------------+
   |                    ||                       ||                                 |
   |                    ||     True              ||                                 |
   |                    |                        ||                                 |
   |        False       +------------------------+|          False                  +
   |                    ||    True               ||                                 |
   |                    ||    False              ||          True                   |
   +--------------------+------------------------+----------------------------------+



Data table
----------
This is an example of a data table that can be rendered using the table directive.
It consists of three columns representing the variables A, B, and A and B respectively.
Each row represents a different combination of True and False for variables A and B.
The `datatable` class can be used to style the data table.

.. code:: rst

    .. table::
        :class: datatable

        =====  =====  =======
        A      B      A and B
        =====  =====  =======
        False  False  False
        True   False  False
        False  True   False
        True   True   True
        =====  =====  =======

.. table::
    :class: datatable

    =====  =====  =======
    A      B      A and B
    =====  =====  =======
    False  False  False
    True   False  False
    False  True   False
    True   True   True
    =====  =====  =======

Longtable-centered
------------------
The longtable-centered class can be used to create a table that
spans multiple pages and is centered horizontally.
This is useful for tables that have a large number of rows or columns.
Here is an example of a longtable-centered:

.. code:: rst

    .. table::
        :class: longtable-centered

        +---------------------------+-------------------+
        |                           | MAPDL Command     |
        +===========================+===================+
        | **GUI commands**          | * ``*ASK``        |
        |                           |                   |
        | **GUI commands**          | * ``*ASK``        |
        |                           |                   |
        | **GUI commands**          | * ``*ASK``        |
        +---------------------------+-------------------+

.. table::
   :class: longtable-centered

   +---------------------------+-------------------+
   |                           | MAPDL Command     |
   +===========================+===================+
   | **GUI commands**          | * ``*ASK``        |
   |                           |                   |
   | **GUI commands**          | * ``*ASK``        |
   |                           |                   |
   | **GUI commands**          | * ``*ASK``        |
   +---------------------------+-------------------+

Table-centered
--------------
The table-centered class can be used to create a table that is horizontally centered.
This is useful for tables that have only a few columns.
Here is an example of a table-centered:

.. code:: rst

    .. table::
        :class: table-centered

        +---------------------------+-------------------+
        |                           | MAPDL Command     |
        +===========================+===================+
        | **GUI commands**          | * ``*ASK``        |
        +---------------------------+-------------------+
        | **GUI commands**          | * ``*ASK``        |
        +---------------------------+-------------------+
        | **GUI commands**          | * ``*ASK``        |
        +---------------------------+-------------------+

.. table::
    :class: table-centered

    +---------------------------+-------------------+
    |                           | MAPDL Command     |
    +===========================+===================+
    | **GUI commands**          | * ``*ASK``        |
    +---------------------------+-------------------+
    | **GUI commands**          | * ``*ASK``        |
    +---------------------------+-------------------+
    | **GUI commands**          | * ``*ASK``        |
    +---------------------------+-------------------+