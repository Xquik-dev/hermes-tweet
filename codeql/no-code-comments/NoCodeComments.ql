// SPDX-FileCopyrightText: 2026 Xquik Contributors
// SPDX-License-Identifier: MIT

/**
 * @name Code comment
 * @description Code has no comments. A comment needs a legal marker, a functional directive or an https link that proves it.
 * @kind problem
 * @problem.severity error
 * @id py/no-code-comments
 */

import python

predicate proven(Comment comment) {
  comment.getText().regexpMatch(".*(https://|SPDX-|REUSE-Ignore).*")
  or
  exists(Comment next |
    next.getLocation().getFile() = comment.getLocation().getFile() and
    next.getLocation().getStartLine() = comment.getLocation().getStartLine() + 1 and
    proven(next)
  )
}

predicate directive(Comment comment) {
  comment.getText().regexpMatch("#\\s*(type:\\s*ignore|noqa|pyright:|mypy:|pragma: no (cover|branch)|fmt: (off|on|skip)|nosec).*")
  or
  comment.getLocation().getStartLine() = 1 and comment.getText().matches("#!%")
}

from Comment comment
where
  exists(comment.getLocation().getFile().getRelativePath()) and
  not proven(comment) and
  not directive(comment)
select comment, "Code has no comments. Put the meaning in names, types and tests."
