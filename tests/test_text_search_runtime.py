import json
import shutil
import subprocess
from unittest.mock import Mock

import pytest

from lumos import Lumos


def test_text_search_does_not_read_ancestor_layout():
    node = shutil.which("node")
    if not node:
        pytest.skip("Node is required to execute the injected JavaScript")
    driver = Mock()
    Lumos(driver).find_by_text("target")
    script = driver.execute_script.call_args.args[0]
    harness = """
      const leaf = {children: [], innerText: 'target', shadowRoot: null};
      const parent = {children: [leaf], shadowRoot: null,
          get innerText() { throw new Error('unnecessary ancestor layout'); }};
      global.document = {querySelectorAll: () => [parent, leaf]};
    """
    harness += "const found = new Function(" + json.dumps(script) + ")('target');"
    harness += "if (found !== leaf) throw new Error('leaf was not found');"
    subprocess.run([node, "-e", harness], check=True, capture_output=True, text=True)
