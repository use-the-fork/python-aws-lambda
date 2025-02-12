{
  description = "A simple flake using the make-shell flake module";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
    flake-parts.url = "github:hercules-ci/flake-parts";
    snow-blower.url = "path:/home/sincore/source/snow-blower";
  };

  nixConfig = {
    extra-experimental-features = "nix-command flakes";

    accept-flake-config = true;
    extra-trusted-public-keys = [
      "cache.nixos.org-1:6NCHdD59X431o0gWypbMrAURkbJ16ZPMQFGspcDShjY="
      "nix-community.cachix.org-1:mB9FSh9qf2dCimDSUo8Zy7bkq5CX+/rkCWyvRCYg3Fs="
      "nixpkgs-unfree.cachix.org-1:hqvoInulhbV4nJ9yJOEr+4wxhDV4xq2d1DK7S6Nj6rs="
      "cache.garnix.io:CTFPyKSLcx5RMJKfLo5EEPUObbA78b0YQ2DTCJXqr9g="
      "devenv.cachix.org-1:w1cLUi8dv3hnoSPGAuibQv+f9TZLr6cv/Hm9XgU50cw="
    ];

    extra-substituters = [
      "https://cache.nixos.org"
      "https://nix-community.cachix.org"
      "https://nixpkgs-unfree.cachix.org"
      "https://cache.garnix.io"
      "https://devenv.cachix.org"
    ];
  };

  outputs = inputs:
    inputs.snow-blower.mkSnowBlower {
      inherit inputs;
      perSystem = {config, ...}: let
        serv = config.snow-blower.services;
        lang = config.snow-blower.languages;
        env = config.snow-blower.env;

        composer = "${lang.php.packages.composer}/bin/composer";
        php = "${lang.php.package}/bin/php";
        npm = "${lang.javascript.npm.package}/bin/npm";

        publicKeys = [
          "ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIOSE69dmDxQ/UJ8k+8CL3lzc/PyJXXO/2aCcYQOjkTW+ sincore@sushi"
        ];

        envKeys = builtins.attrNames config.snow-blower.env;
        unsetEnv = builtins.concatStringsSep "\n" (
          map (key: "unset ${key}") envKeys
        );
      in {
        snow-blower = {
          paths.src = ./.;
          dotenv.enable = true;


          scripts = {

          };

          processes = {

          };

          languages = {
            python = {
              enable = true;
              poetry = {
                enable = true;
                install.enable = true;
                activate.enable = true;
              };
            };
          };

          services = {
            aider = {
              enable = true;
            };
          };

          integrations = {
            agenix = {
              enable = true;
              secrets = {
                ".env" = {
                  inherit publicKeys;
                };
              };
            };

            git-cliff.enable = true;

            treefmt = {
              programs = {
                alejandra.enable = true;
              };
            };

            git-hooks.hooks = {
              treefmt = {
                enable = true;
              };
            };
          };
        };
      };
    };
}
