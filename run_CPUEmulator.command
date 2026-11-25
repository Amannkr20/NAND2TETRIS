#!/bin/bash
export PATH="/opt/homebrew/Cellar/openjdk/26.0.2/bin:$PATH"
cd "$(dirname "$0")/nand2tetris_tools"
java -classpath ":bin/classes:bin/lib/Hack.jar:bin/lib/HackGUI.jar:bin/lib/Simulators.jar:bin/lib/SimulatorsGUI.jar:bin/lib/Compilers.jar" CPUEmulatorMain "$@"
