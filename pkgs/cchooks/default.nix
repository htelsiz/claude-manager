{ python3Packages }:

python3Packages.buildPythonPackage {
  pname = "cchooks";
  version = "0.2.0";
  src = ./.;
  format = "pyproject";
  nativeBuildInputs = [ python3Packages.setuptools ];
}
