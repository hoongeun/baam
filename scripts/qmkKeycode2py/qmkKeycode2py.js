/**
 * qmkKeyCode2py
 * This script download from qmk github repository and convert to micropython(circuitpython) optimzed keycodes file
 */

import got from "got";
import { writeFile } from "node:fs/promises";

const [nodePath, scriptPath, ...args] = process.argv.filter((arg) => arg !== "node");

async function main() {
  await Promise.all(
    args.map(async (arg) => {
      const { body } = await got.get(
        `https://raw.githubusercontent.com/qmk/qmk_firmware/master/data/constants/keycodes/keycodes_0.0.1_${arg}.hjson`
      );
      const constized = Object.entries(JSON.parse(body).keycodes).reduce(
        (acc, [keycode, val]) => {
          acc[val.key] = `const(${keycode})`;
          if ("aliases" in val) {
            val.aliases.forEach((alias) => {
              acc[alias] = `const(${keycode})`;
            });
          }
          return acc;
        },
        {}
      );
      let result = "from micropython import const\n\n\n"
      result += `${arg} = ${JSON.stringify(constized, null, 4)}`
      await writeFile(`outputs/${arg}_keycode.py`, result);
      return constized;
    })
  );
}

main()
