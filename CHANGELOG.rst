Changelog
=========

django-fsm 5.0.2 2026-11-13
~~~~~~~~~~~~~~~~~~~~~~~~~~~

- Fix ``chart()`` for states that are plain ``Enum`` members: the edges were
  named with ``str(member)`` while the vertices used the member value, so no
  edge was attached to a vertex.
- Fix ``chart()`` missing edges between the targets of several
  ``State.ANY`` transitions: only the transitions processed later got an edge
  from the targets of the earlier ones.
- ``chart()`` no longer produces invalid DOT for state names and transition
  labels that contain a double quote. Graphviz and the vis-network parser
  disagree on how a quote is escaped, so it is replaced with a typographic one.
- Fix ``State.get()`` ignoring a falsy default (``0``, ``False``, ``""``): a
  state getter returning ``None`` now reads as that default.
- Strip the extra blank line at the end of ``base.py`` and ``signals.py``.


django-fsm 5.0.1 2026-10-27
~~~~~~~~~~~~~~~~~~~~~~~~~~~

- Fix ``from django_fsm import *`` without Django installed by exporting only
  the available core API, and add regression tests for both import modes.
- Document the 5.0 transition timing change and clarify that direct transition
  calls do not check user permissions automatically.
- Include CONTRIBUTING.rst in source distributions and link to it on GitHub.
- Update the package homepage to https://github.com/viewflow/django-fsm.


django-fsm 5.0.0 2026-10-27
~~~~~~~~~~~~~~~~~~~~~~~~~~~

- Restore django-fsm as an independently maintained package with Viewflow FSM
  engine under the hood.
- Make Django dependency optional: the pure-Python ``State`` API, ``chart()``,
  ``can_proceed()``, and ``has_transition_perm()`` work without Django installed.
- Django model adapters (``FSMField``, ``FSMIntegerField``, ``FSMKeyField``) and
  ``@transition(field=...)`` are available with Django installed or via
  ``pip install 'django-fsm[django]'``.
- Add ``State``, forward references (``this``), dynamic targets (``RETURN_VALUE``,
  ``GET_STATE``), and optional Viewflow Pro / DRF modules.
- Preserve backward-compatible APIs for model-backed fields, conditions, permissions,
  signals, error targets, and optimistic locking (``ConcurrentTransitionMixin``).
- Change transition timing: ordinary targets and ``GET_STATE`` apply before
  the method body runs, unlike django-fsm 3.x. ``RETURN_VALUE`` applies after
  the method returns. Restoring state in memory does not roll back database writes.
- Require Python 3.10+; Django 5.2+ / 6.0+ supported.
- Use AGPL-3.0-or-later with the Viewflow Library Exception, retaining the original
  MIT notice in LICENSE_LEGACY.


django-fsm 3.0.1 2025-10-07
~~~~~~~~~~~~~~~~~~~~~~~~~~~

- Add Django 6.0 support
- Update tox.ini to test against latest Django versions (5.1, 5.2, 6.0a1)
- Fix ConcurrentTransitionMixin._do_update() for Django 6.0 compatibility
- Update Django versions in tox.ini to latest patch releases


django-fsm 2.8.2 2024-04-09
~~~~~~~~~~~~~~~~~~~~~~~~~~~

- Fix graph_transitions commnad for Django>=4.0
- Preserve chosen "using" DB in ConcurentTransitionMixin
- Fix error message in GET_STATE
- Implement Transition __hash__ and __eq__ for 'in' operator


django-fsm 2.8.1 2022-08-15
~~~~~~~~~~~~~~~~~~~~~~~~~~~

- Improve fix for get_available_FIELD_transition


django-fsm 2.8.0 2021-11-05
~~~~~~~~~~~~~~~~~~~~~~~~~~

- Fix get_available_FIELD_transition on django>=3.2
- Fix refresh_from_db for ConcurrentTransitionMixin


django-fsm 2.7.1 2020-10-13
~~~~~~~~~~~~~~~~~~~~~~~~~~

- Fix warnings on Django 3.1+


django-fsm 2.7.0 2019-12-03
~~~~~~~~~~~~~~~~~~~~~~~~~~~

- Django 3.0 support
- Test on Python 3.8


django-fsm 2.6.1 2019-04-19
~~~~~~~~~~~~~~~~~~~~~~~~~~~

- Update pypi classifiers to latest django/python supported versions
- Several fixes for graph_transition command


django-fsm 2.6.0 2017-06-08
~~~~~~~~~~~~~~~~~~~~~~~~~~~

- Fix django 1.11 compatibility
- Fix TypeError in `graph_transitions` command when using django's lazy translations


django-fsm 2.5.0 2017-03-04
~~~~~~~~~~~~~~~~~~~~~~~~~~~

- graph_transition command fix for django 1.10
- graph_transition command supports GET_STATE targets
- signal data extended with method args/kwargs and field
- sets allowed to be passed to the transition decorator


django-fsm 2.4.0 2016-05-14
~~~~~~~~~~~~~~~~~~~~~~~~~~~

- graph_transition commnad now works with multiple  FSM's per model
- Add ability to set target state from transition return value or callable


django-fsm 2.3.0 2015-10-15
~~~~~~~~~~~~~~~~~~~~~~~~~~~

- Add source state shortcut '+' to specify transitions from all states except the target
- Add object-level permission checks
- Fix translated labels for graph of FSMIntegerField
- Fix multiple signals for several transition decorators


django-fsm 2.2.1 2015-04-27
~~~~~~~~~~~~~~~~~~~~~~~~~~~

- Improved exception message for unmet transition conditions.
- Don't send post transition signal in case of no state changes on
  exception
- Allow empty string as correct state value
- Improved graphviz fsm visualisation
- Clean django 1.8 warnings

django-fsm 2.2.0 2014-09-03
~~~~~~~~~~~~~~~~~~~~~~~~~~~

- Support for `class
  substitution <http://schinckel.net/2013/06/13/django-proxy-model-state-machine/>`__
  to proxy classes depending on the state
- Added ConcurrentTransitionMixin with optimistic locking support
- Default db\_index=True for FSMIntegerField removed
- Graph transition code migrated to new graphviz library with python 3
  support
- Ability to change state on transition exception

django-fsm 2.1.0 2014-05-15
~~~~~~~~~~~~~~~~~~~~~~~~~~~

- Support for attaching permission checks on model transitions

django-fsm 2.0.0 2014-03-15
~~~~~~~~~~~~~~~~~~~~~~~~~~~

- Backward incompatible release
- All public code import moved directly to django\_fsm package
- Correct support for several @transitions decorator with different
  source states and conditions on same method
- save parameter from transition decorator removed
- get\_available\_FIELD\_transitions return Transition data object
  instead of tuple
- Models got get\_available\_FIELD\_transitions, even if field
  specified as string reference
- New get\_all\_FIELD\_transitions method contributed to class

django-fsm 1.6.0 2014-03-15
~~~~~~~~~~~~~~~~~~~~~~~~~~~

- FSMIntegerField and FSMKeyField support

django-fsm 1.5.1 2014-01-04
~~~~~~~~~~~~~~~~~~~~~~~~~~~

- Ad-hoc support for state fields from proxy and inherited models

django-fsm 1.5.0 2013-09-17
~~~~~~~~~~~~~~~~~~~~~~~~~~~

- Python 3 compatibility

django-fsm 1.4.0 2011-12-21
~~~~~~~~~~~~~~~~~~~~~~~~~~~

- Add graph\_transition command for drawing state transition picture

django-fsm 1.3.0 2011-07-28
~~~~~~~~~~~~~~~~~~~~~~~~~~~

- Add direct field modification protection

django-fsm 1.2.0 2011-03-23
~~~~~~~~~~~~~~~~~~~~~~~~~~~

- Add pre\_transition and post\_transition signals

django-fsm 1.1.0 2011-02-22
~~~~~~~~~~~~~~~~~~~~~~~~~~~

- Add support for transition conditions
- Allow multiple FSMField in one model
- Contribute get\_available\_FIELD\_transitions for model class

django-fsm 1.0.0 2010-10-12
~~~~~~~~~~~~~~~~~~~~~~~~~~~

- Initial public release
