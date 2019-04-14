### Global commands

| Name | Description | Internal name |
| === | === | === |
| load | Load a file and type check it. | `Cmd_Load` |
| compile | compile a file using the various agda backends (`GHC`, `GHCNoMain`, `LaTeX`, `QuickLaTeX` etc) | `Cmd_compile` |
| abort | abort the current operation, do nothing otherwise | `Cmd_abort` |
| toggle-display-of-implicit-arguments | | `ToggleImplicitArgs` |
| show-constraints | Show constraints or goals | `Cmd_constraints` |
| solve-constraints | Solve all constraints in a file | `Cmd_solveAll` |
| show-goals | Show all goals in a file | `Cmd_metas` |
| search-about | Search about a keyword | `Cmd_search_about_toplevel` |

### Goal-specific commands

| Name | Description | Internal name |
| === | === | === |
| why-in-scope | Explain why a keyword is in scope | `Cmd_why_in_scope` |
| infer-type | Infer type | `Cmd_infer` |
| module-contents | List all module contents | `Cmd_show_module_contents` |
| compute-normal-form | Compute the normal form of either selected code or given expression | `Cmd_compute` |

### Commands working in the context of a specific goal

| Name | Description | Internal name |
| === | === | === |
| give | Fill a goal | `Cmd_give` |
| refine | Refine. Partial give: makes new holes for missing arguments | `Cmd_refine_or_intro` |
| auto | Automatic proof search, find proofs | `Cmd_auto` |
| case | Pattern match on variables (case split) | `Cmd_make_case` |
| goal-type | Goal type | `Cmd_goal_type` |
| context | Context of the goal | `Cmd_context` |
| goal-type-and-context | Type and context of the goal | `Cmd_goal_type_context` |
| goal-type-and-inferred-type | Infer goal type and the context of the goal | `Cmd_goal_type_context_infer` |



