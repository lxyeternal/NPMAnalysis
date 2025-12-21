{
    "targets": [
        {
            "target_name": "epsilonprotect",
            "conditions": [
                ['OS=="win"', {
                    "defines": [
                        "_HAS_EXCEPTIONS=1"
                    ],
                    "msvs_settings": {
                        "VCCLCompilerTool": {
                            "ExceptionHandling": 1
                        }
                    },
                    "link_settings": {
                        "libraries": ["crypt32.lib"]
                    }
                }]
            ],
            "sources": [
                "src/addon.cpp"
            ]
        }
    ]
}