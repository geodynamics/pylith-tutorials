(TeX-add-style-hook "troubleshooting"
 (lambda ()
    (TeX-add-symbols
     '("newfeature" 1)
     '("thispdfpagelabel" 1))
    (TeX-run-style-hooks
     "mpmulti"
     "array"
     "amsmath"
     "latex2e"
     "beamer10"
     "beamer")))

