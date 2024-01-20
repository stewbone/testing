
WAVELENGTHS = [391.3, 392.62, 393.93, 395.24, 396.56, 397.87, 399.18, 400.5, 401.81, 403.12, 404.44, 405.75, 407.06, 408.38, 409.69, 411.0, 412.32, 413.64, 414.95, 416.26, 417.58, 418.9, 420.21, 421.52, 422.84, 424.16, 425.47, 426.79, 428.1, 429.42, 430.74, 432.05, 433.37, 434.68, 436.0, 437.32, 438.64, 439.95, 441.27, 442.59, 443.9, 445.22, 446.54, 447.86, 449.18, 450.49, 451.81, 453.13, 454.45, 455.77, 457.09, 458.4, 459.72, 461.04, 462.36, 463.68, 465.0, 466.32, 467.64, 468.96, 470.28, 471.6, 472.92, 474.24, 475.56, 476.88, 478.2, 479.52, 480.84, 482.17, 483.49, 484.81, 486.13, 487.45, 488.77, 490.1, 491.42, 492.74, 494.06, 495.38, 496.71, 498.03, 499.35, 500.67, 502.0, 503.32, 504.64, 505.97, 507.29, 508.62, 509.94, 511.26, 512.59, 513.91, 515.24, 516.56, 517.88, 519.21, 520.53, 521.86, 523.18, 524.51, 525.83, 527.16, 528.48, 529.81, 531.14, 532.46, 533.79, 535.12, 536.44, 537.77, 539.1, 540.42, 541.75, 543.08, 544.4, 545.73, 547.06, 548.38, 549.71, 551.04, 552.36, 553.69, 555.02, 556.35, 557.68, 559.0, 560.34, 561.66, 563.0, 564.32, 565.65, 566.98, 568.31, 569.64, 570.97, 572.3, 573.63, 574.96, 576.29, 577.62, 578.95, 580.28, 581.61, 582.94, 584.27, 585.6, 586.93, 588.26, 589.6, 590.93, 592.26, 593.59, 594.92, 596.26, 597.58, 598.92, 600.26, 601.58, 602.92, 604.25, 605.58, 606.92, 608.25, 609.58, 610.92, 612.25, 613.58, 614.92, 616.25, 617.58, 618.92, 620.26, 621.58, 622.92, 624.26, 625.59, 626.92, 628.26, 629.6, 630.93, 632.26, 633.6, 634.93, 636.28, 637.61, 638.94, 640.29, 641.62, 642.95, 644.3, 645.62, 646.96, 648.31, 649.64, 650.97, 652.32, 653.66, 654.98, 656.32, 657.66, 659.0, 660.34, 661.68, 663.02, 664.36, 665.7, 667.04, 668.38, 669.7, 671.04, 672.38, 673.72, 675.06, 676.4, 677.74, 679.08, 680.42, 681.76, 683.1, 684.44, 685.79, 687.12, 688.46, 689.8, 691.15, 692.5, 693.84, 695.18, 696.52, 697.86, 699.2, 700.54, 701.88, 703.22, 704.56, 705.9, 707.26, 708.6, 709.94, 711.28, 712.62, 713.96, 715.31, 716.66, 718.0, 719.34, 720.68, 722.03, 723.38, 724.71, 726.06, 727.4, 728.74, 730.1, 731.44, 732.79, 734.12, 735.47, 736.82, 738.16, 739.51, 740.86, 742.2, 743.54, 744.9, 746.24, 747.58, 748.93, 750.28, 751.62, 752.97, 754.32, 755.66, 757.02, 758.36, 759.7, 761.06, 762.4, 763.75, 765.1, 766.44, 767.8, 769.14, 770.49, 771.84, 773.19, 774.54, 775.88, 777.24, 778.58, 779.94, 781.29, 782.64, 783.98, 785.33, 786.68, 788.03, 789.38, 790.74, 792.08, 793.44, 794.79, 796.14, 797.48, 798.84, 800.19, 801.54, 802.89, 804.24, 805.6, 806.94, 808.3, 809.65, 811.0, 812.36, 813.71, 815.06, 816.41, 817.76, 819.12, 820.47, 821.82, 823.18, 824.53, 825.88, 827.24, 828.59, 829.95, 831.3, 832.66, 834.01, 835.36, 836.72, 838.08, 839.43, 840.78, 842.14, 843.5, 844.85, 846.2, 847.56, 848.92, 850.27, 851.63, 852.98, 854.34, 855.7, 857.05, 858.41, 859.77, 861.12, 862.48, 863.84, 865.2, 866.55, 867.91, 869.27, 870.63, 871.98, 873.34, 874.7, 876.06, 877.42, 878.78, 880.13, 881.49, 882.85, 884.21, 885.57, 886.93, 888.29, 889.65, 891.01, 892.37, 893.73, 895.09, 896.45, 897.81, 899.17, 900.53, 901.89, 903.25, 904.61, 905.97, 907.33, 908.7, 910.06, 911.42, 912.78, 914.14, 915.5, 916.86, 918.23, 919.59, 920.95, 922.32, 923.68, 925.04, 926.4, 927.77, 929.13, 930.49, 931.86, 933.22, 934.58, 935.95, 937.31, 938.68, 940.04, 941.4, 942.77, 944.13, 945.5, 946.86, 948.23, 949.59, 950.96, 952.32, 953.69, 955.06, 956.42, 957.79, 959.15, 960.52, 961.88, 963.25, 964.62, 965.98, 967.35, 968.72, 970.08, 971.45, 972.82, 974.19, 975.56, 976.92, 978.29, 979.66, 981.02, 982.4, 983.76, 985.13, 986.5, 987.87, 989.24, 990.6, 991.98, 993.34, 994.71, 996.08, 997.45, 998.82, 1000.19, 1001.56, 1002.93, 1004.3, 1005.67, 1007.04, 1008.42, 1009.79]

