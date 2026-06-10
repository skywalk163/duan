# Generated from DuanLangParser.g4 by ANTLR 4.13.2
# encoding: utf-8
from antlr4 import *
from io import StringIO
import sys
if sys.version_info[1] > 5:
	from typing import TextIO
else:
	from typing.io import TextIO


from typing import List, Optional, Tuple, Any, Union

def serializedATN():
    return [
        4,1,100,496,2,0,7,0,2,1,7,1,2,2,7,2,2,3,7,3,2,4,7,4,2,5,7,5,2,6,
        7,6,2,7,7,7,2,8,7,8,2,9,7,9,2,10,7,10,2,11,7,11,2,12,7,12,2,13,7,
        13,2,14,7,14,2,15,7,15,2,16,7,16,2,17,7,17,2,18,7,18,2,19,7,19,2,
        20,7,20,2,21,7,21,2,22,7,22,2,23,7,23,2,24,7,24,2,25,7,25,2,26,7,
        26,2,27,7,27,2,28,7,28,2,29,7,29,2,30,7,30,2,31,7,31,2,32,7,32,2,
        33,7,33,2,34,7,34,2,35,7,35,2,36,7,36,2,37,7,37,2,38,7,38,2,39,7,
        39,2,40,7,40,2,41,7,41,2,42,7,42,2,43,7,43,2,44,7,44,2,45,7,45,1,
        0,1,0,1,0,1,0,1,0,5,0,98,8,0,10,0,12,0,101,9,0,1,0,1,0,1,1,1,1,1,
        1,1,1,1,2,1,2,1,2,3,2,112,8,2,1,3,1,3,1,3,1,3,1,3,1,3,3,3,120,8,
        3,1,3,1,3,1,3,3,3,125,8,3,1,3,1,3,1,3,1,3,3,3,131,8,3,1,4,1,4,1,
        4,5,4,136,8,4,10,4,12,4,139,9,4,1,5,1,5,1,5,3,5,144,8,5,1,5,1,5,
        3,5,148,8,5,1,6,5,6,151,8,6,10,6,12,6,154,9,6,1,7,1,7,1,7,1,7,1,
        7,1,7,4,7,162,8,7,11,7,12,7,163,1,7,1,7,3,7,168,8,7,1,8,1,8,1,8,
        1,8,3,8,174,8,8,1,9,1,9,1,9,1,9,1,9,1,9,4,9,182,8,9,11,9,12,9,183,
        1,9,1,9,3,9,188,8,9,1,10,1,10,1,10,1,10,1,10,3,10,195,8,10,1,10,
        1,10,1,10,3,10,200,8,10,3,10,202,8,10,1,11,1,11,1,11,1,11,1,11,3,
        11,209,8,11,1,11,3,11,212,8,11,1,12,1,12,1,12,5,12,217,8,12,10,12,
        12,12,220,9,12,1,13,1,13,1,13,5,13,225,8,13,10,13,12,13,228,9,13,
        1,14,1,14,1,14,1,14,3,14,234,8,14,1,15,1,15,1,15,1,15,1,15,1,15,
        1,15,1,15,1,15,1,15,1,15,1,15,3,15,248,8,15,1,16,1,16,1,16,1,16,
        3,16,254,8,16,1,16,3,16,257,8,16,1,17,1,17,1,17,1,17,3,17,263,8,
        17,1,18,1,18,1,18,1,18,1,18,3,18,270,8,18,1,19,1,19,1,19,1,19,1,
        19,3,19,277,8,19,1,19,1,19,1,19,1,19,1,19,1,19,5,19,285,8,19,10,
        19,12,19,288,9,19,1,19,1,19,1,19,3,19,293,8,19,1,19,1,19,3,19,297,
        8,19,1,20,1,20,1,20,1,20,1,20,3,20,304,8,20,1,20,1,20,3,20,308,8,
        20,1,21,1,21,1,21,1,21,1,21,1,21,1,21,1,21,1,21,3,21,319,8,21,1,
        22,1,22,1,22,1,22,3,22,325,8,22,1,22,1,22,3,22,329,8,22,1,23,1,23,
        3,23,333,8,23,1,23,3,23,336,8,23,1,24,1,24,3,24,340,8,24,1,25,1,
        25,3,25,344,8,25,1,26,1,26,1,26,1,26,1,26,1,26,1,26,1,26,1,26,3,
        26,355,8,26,1,27,1,27,1,27,3,27,360,8,27,1,28,1,28,1,28,3,28,365,
        8,28,1,29,1,29,3,29,369,8,29,1,30,1,30,1,31,1,31,1,31,5,31,376,8,
        31,10,31,12,31,379,9,31,1,32,1,32,1,32,5,32,384,8,32,10,32,12,32,
        387,9,32,1,33,1,33,1,33,5,33,392,8,33,10,33,12,33,395,9,33,1,34,
        1,34,1,34,1,34,5,34,401,8,34,10,34,12,34,404,9,34,1,35,1,35,1,36,
        1,36,1,36,1,36,5,36,412,8,36,10,36,12,36,415,9,36,1,37,1,37,1,38,
        1,38,1,38,1,38,5,38,423,8,38,10,38,12,38,426,9,38,1,39,1,39,1,40,
        1,40,1,40,1,40,1,40,3,40,435,8,40,1,41,1,41,1,41,1,41,1,41,1,41,
        3,41,443,8,41,1,41,1,41,1,41,3,41,448,8,41,1,41,1,41,1,41,1,41,1,
        41,1,41,1,41,5,41,457,8,41,10,41,12,41,460,9,41,1,42,1,42,1,42,1,
        42,1,42,1,42,1,42,1,42,1,42,1,42,1,42,1,42,3,42,474,8,42,1,42,1,
        42,1,42,1,42,3,42,480,8,42,1,43,1,43,3,43,484,8,43,1,44,1,44,1,45,
        1,45,1,45,5,45,491,8,45,10,45,12,45,494,9,45,1,45,0,0,46,0,2,4,6,
        8,10,12,14,16,18,20,22,24,26,28,30,32,34,36,38,40,42,44,46,48,50,
        52,54,56,58,60,62,64,66,68,70,72,74,76,78,80,82,84,86,88,90,0,8,
        1,0,33,34,2,0,50,50,80,80,3,0,10,14,16,16,71,76,2,0,44,45,69,70,
        2,0,46,49,65,68,2,0,43,43,77,77,2,0,45,45,70,70,1,0,55,64,534,0,
        99,1,0,0,0,2,104,1,0,0,0,4,111,1,0,0,0,6,113,1,0,0,0,8,132,1,0,0,
        0,10,140,1,0,0,0,12,152,1,0,0,0,14,155,1,0,0,0,16,169,1,0,0,0,18,
        175,1,0,0,0,20,201,1,0,0,0,22,203,1,0,0,0,24,213,1,0,0,0,26,221,
        1,0,0,0,28,233,1,0,0,0,30,247,1,0,0,0,32,249,1,0,0,0,34,258,1,0,
        0,0,36,269,1,0,0,0,38,271,1,0,0,0,40,298,1,0,0,0,42,318,1,0,0,0,
        44,320,1,0,0,0,46,330,1,0,0,0,48,337,1,0,0,0,50,341,1,0,0,0,52,345,
        1,0,0,0,54,356,1,0,0,0,56,361,1,0,0,0,58,366,1,0,0,0,60,370,1,0,
        0,0,62,372,1,0,0,0,64,380,1,0,0,0,66,388,1,0,0,0,68,396,1,0,0,0,
        70,405,1,0,0,0,72,407,1,0,0,0,74,416,1,0,0,0,76,418,1,0,0,0,78,427,
        1,0,0,0,80,434,1,0,0,0,82,436,1,0,0,0,84,479,1,0,0,0,86,483,1,0,
        0,0,88,485,1,0,0,0,90,487,1,0,0,0,92,98,3,2,1,0,93,98,3,20,10,0,
        94,98,3,22,11,0,95,98,3,4,2,0,96,98,3,30,15,0,97,92,1,0,0,0,97,93,
        1,0,0,0,97,94,1,0,0,0,97,95,1,0,0,0,97,96,1,0,0,0,98,101,1,0,0,0,
        99,97,1,0,0,0,99,100,1,0,0,0,100,102,1,0,0,0,101,99,1,0,0,0,102,
        103,5,0,0,1,103,1,1,0,0,0,104,105,5,89,0,0,105,106,5,97,0,0,106,
        107,5,90,0,0,107,3,1,0,0,0,108,112,3,6,3,0,109,112,3,14,7,0,110,
        112,3,18,9,0,111,108,1,0,0,0,111,109,1,0,0,0,111,110,1,0,0,0,112,
        5,1,0,0,0,113,114,5,93,0,0,114,115,5,97,0,0,115,116,5,94,0,0,116,
        117,5,17,0,0,117,119,5,87,0,0,118,120,3,8,4,0,119,118,1,0,0,0,119,
        120,1,0,0,0,120,121,1,0,0,0,121,124,5,88,0,0,122,123,5,80,0,0,123,
        125,3,86,43,0,124,122,1,0,0,0,124,125,1,0,0,0,125,126,1,0,0,0,126,
        127,5,84,0,0,127,128,3,12,6,0,128,130,5,9,0,0,129,131,5,82,0,0,130,
        129,1,0,0,0,130,131,1,0,0,0,131,7,1,0,0,0,132,137,3,10,5,0,133,134,
        5,83,0,0,134,136,3,10,5,0,135,133,1,0,0,0,136,139,1,0,0,0,137,135,
        1,0,0,0,137,138,1,0,0,0,138,9,1,0,0,0,139,137,1,0,0,0,140,143,5,
        97,0,0,141,142,5,84,0,0,142,144,3,86,43,0,143,141,1,0,0,0,143,144,
        1,0,0,0,144,147,1,0,0,0,145,146,5,16,0,0,146,148,3,60,30,0,147,145,
        1,0,0,0,147,148,1,0,0,0,148,11,1,0,0,0,149,151,3,30,15,0,150,149,
        1,0,0,0,151,154,1,0,0,0,152,150,1,0,0,0,152,153,1,0,0,0,153,13,1,
        0,0,0,154,152,1,0,0,0,155,156,5,93,0,0,156,157,5,97,0,0,157,158,
        5,94,0,0,158,159,5,18,0,0,159,161,5,84,0,0,160,162,3,16,8,0,161,
        160,1,0,0,0,162,163,1,0,0,0,163,161,1,0,0,0,163,164,1,0,0,0,164,
        165,1,0,0,0,165,167,5,9,0,0,166,168,5,82,0,0,167,166,1,0,0,0,167,
        168,1,0,0,0,168,15,1,0,0,0,169,170,5,97,0,0,170,171,5,84,0,0,171,
        173,3,86,43,0,172,174,5,82,0,0,173,172,1,0,0,0,173,174,1,0,0,0,174,
        17,1,0,0,0,175,176,5,93,0,0,176,177,5,97,0,0,177,178,5,94,0,0,178,
        179,5,19,0,0,179,181,5,84,0,0,180,182,3,16,8,0,181,180,1,0,0,0,182,
        183,1,0,0,0,183,181,1,0,0,0,183,184,1,0,0,0,184,185,1,0,0,0,185,
        187,5,9,0,0,186,188,5,82,0,0,187,186,1,0,0,0,187,188,1,0,0,0,188,
        19,1,0,0,0,189,190,5,24,0,0,190,191,3,24,12,0,191,192,5,23,0,0,192,
        194,3,26,13,0,193,195,5,82,0,0,194,193,1,0,0,0,194,195,1,0,0,0,195,
        202,1,0,0,0,196,197,5,23,0,0,197,199,3,26,13,0,198,200,5,82,0,0,
        199,198,1,0,0,0,199,200,1,0,0,0,200,202,1,0,0,0,201,189,1,0,0,0,
        201,196,1,0,0,0,202,21,1,0,0,0,203,208,5,22,0,0,204,209,5,97,0,0,
        205,206,5,93,0,0,206,207,5,97,0,0,207,209,5,94,0,0,208,204,1,0,0,
        0,208,205,1,0,0,0,209,211,1,0,0,0,210,212,5,82,0,0,211,210,1,0,0,
        0,211,212,1,0,0,0,212,23,1,0,0,0,213,218,5,97,0,0,214,215,5,81,0,
        0,215,217,5,97,0,0,216,214,1,0,0,0,217,220,1,0,0,0,218,216,1,0,0,
        0,218,219,1,0,0,0,219,25,1,0,0,0,220,218,1,0,0,0,221,226,3,28,14,
        0,222,223,5,83,0,0,223,225,3,28,14,0,224,222,1,0,0,0,225,228,1,0,
        0,0,226,224,1,0,0,0,226,227,1,0,0,0,227,27,1,0,0,0,228,226,1,0,0,
        0,229,230,5,93,0,0,230,231,5,97,0,0,231,234,5,94,0,0,232,234,5,97,
        0,0,233,229,1,0,0,0,233,232,1,0,0,0,234,29,1,0,0,0,235,248,3,32,
        16,0,236,248,3,34,17,0,237,248,3,38,19,0,238,248,3,40,20,0,239,248,
        3,44,22,0,240,248,3,46,23,0,241,248,3,48,24,0,242,248,3,50,25,0,
        243,248,3,52,26,0,244,248,3,54,27,0,245,248,3,56,28,0,246,248,3,
        58,29,0,247,235,1,0,0,0,247,236,1,0,0,0,247,237,1,0,0,0,247,238,
        1,0,0,0,247,239,1,0,0,0,247,240,1,0,0,0,247,241,1,0,0,0,247,242,
        1,0,0,0,247,243,1,0,0,0,247,244,1,0,0,0,247,245,1,0,0,0,247,246,
        1,0,0,0,248,31,1,0,0,0,249,250,5,15,0,0,250,253,5,97,0,0,251,252,
        5,16,0,0,252,254,3,60,30,0,253,251,1,0,0,0,253,254,1,0,0,0,254,256,
        1,0,0,0,255,257,5,82,0,0,256,255,1,0,0,0,256,257,1,0,0,0,257,33,
        1,0,0,0,258,259,3,36,18,0,259,260,5,16,0,0,260,262,3,60,30,0,261,
        263,5,82,0,0,262,261,1,0,0,0,262,263,1,0,0,0,263,35,1,0,0,0,264,
        270,5,97,0,0,265,266,3,60,30,0,266,267,5,51,0,0,267,268,5,97,0,0,
        268,270,1,0,0,0,269,264,1,0,0,0,269,265,1,0,0,0,270,37,1,0,0,0,271,
        272,5,6,0,0,272,273,3,60,30,0,273,276,5,7,0,0,274,275,5,84,0,0,275,
        277,3,12,6,0,276,274,1,0,0,0,276,277,1,0,0,0,277,286,1,0,0,0,278,
        279,5,5,0,0,279,280,3,60,30,0,280,281,5,7,0,0,281,282,5,84,0,0,282,
        283,3,12,6,0,283,285,1,0,0,0,284,278,1,0,0,0,285,288,1,0,0,0,286,
        284,1,0,0,0,286,287,1,0,0,0,287,292,1,0,0,0,288,286,1,0,0,0,289,
        290,5,8,0,0,290,291,5,84,0,0,291,293,3,12,6,0,292,289,1,0,0,0,292,
        293,1,0,0,0,293,294,1,0,0,0,294,296,5,9,0,0,295,297,5,82,0,0,296,
        295,1,0,0,0,296,297,1,0,0,0,297,39,1,0,0,0,298,299,5,25,0,0,299,
        300,3,42,21,0,300,303,3,60,30,0,301,302,5,84,0,0,302,304,3,12,6,
        0,303,301,1,0,0,0,303,304,1,0,0,0,304,305,1,0,0,0,305,307,5,9,0,
        0,306,308,5,82,0,0,307,306,1,0,0,0,307,308,1,0,0,0,308,41,1,0,0,
        0,309,319,5,97,0,0,310,311,5,97,0,0,311,312,5,51,0,0,312,319,5,97,
        0,0,313,314,5,97,0,0,314,315,5,51,0,0,315,316,5,97,0,0,316,317,5,
        83,0,0,317,319,5,97,0,0,318,309,1,0,0,0,318,310,1,0,0,0,318,313,
        1,0,0,0,319,43,1,0,0,0,320,321,5,26,0,0,321,324,3,60,30,0,322,323,
        5,84,0,0,323,325,3,12,6,0,324,322,1,0,0,0,324,325,1,0,0,0,325,326,
        1,0,0,0,326,328,5,9,0,0,327,329,5,82,0,0,328,327,1,0,0,0,328,329,
        1,0,0,0,329,45,1,0,0,0,330,332,5,32,0,0,331,333,3,60,30,0,332,331,
        1,0,0,0,332,333,1,0,0,0,333,335,1,0,0,0,334,336,5,82,0,0,335,334,
        1,0,0,0,335,336,1,0,0,0,336,47,1,0,0,0,337,339,5,27,0,0,338,340,
        5,82,0,0,339,338,1,0,0,0,339,340,1,0,0,0,340,49,1,0,0,0,341,343,
        5,28,0,0,342,344,5,82,0,0,343,342,1,0,0,0,343,344,1,0,0,0,344,51,
        1,0,0,0,345,346,5,29,0,0,346,347,5,84,0,0,347,348,3,12,6,0,348,349,
        5,30,0,0,349,350,5,97,0,0,350,351,5,84,0,0,351,352,3,12,6,0,352,
        354,5,9,0,0,353,355,5,82,0,0,354,353,1,0,0,0,354,355,1,0,0,0,355,
        53,1,0,0,0,356,357,5,31,0,0,357,359,3,60,30,0,358,360,5,82,0,0,359,
        358,1,0,0,0,359,360,1,0,0,0,360,55,1,0,0,0,361,362,7,0,0,0,362,364,
        3,60,30,0,363,365,5,82,0,0,364,363,1,0,0,0,364,365,1,0,0,0,365,57,
        1,0,0,0,366,368,3,60,30,0,367,369,5,82,0,0,368,367,1,0,0,0,368,369,
        1,0,0,0,369,59,1,0,0,0,370,371,3,62,31,0,371,61,1,0,0,0,372,377,
        3,64,32,0,373,374,7,1,0,0,374,376,3,64,32,0,375,373,1,0,0,0,376,
        379,1,0,0,0,377,375,1,0,0,0,377,378,1,0,0,0,378,63,1,0,0,0,379,377,
        1,0,0,0,380,385,3,66,33,0,381,382,5,41,0,0,382,384,3,66,33,0,383,
        381,1,0,0,0,384,387,1,0,0,0,385,383,1,0,0,0,385,386,1,0,0,0,386,
        65,1,0,0,0,387,385,1,0,0,0,388,393,3,68,34,0,389,390,5,42,0,0,390,
        392,3,68,34,0,391,389,1,0,0,0,392,395,1,0,0,0,393,391,1,0,0,0,393,
        394,1,0,0,0,394,67,1,0,0,0,395,393,1,0,0,0,396,402,3,72,36,0,397,
        398,3,70,35,0,398,399,3,72,36,0,399,401,1,0,0,0,400,397,1,0,0,0,
        401,404,1,0,0,0,402,400,1,0,0,0,402,403,1,0,0,0,403,69,1,0,0,0,404,
        402,1,0,0,0,405,406,7,2,0,0,406,71,1,0,0,0,407,413,3,76,38,0,408,
        409,3,74,37,0,409,410,3,76,38,0,410,412,1,0,0,0,411,408,1,0,0,0,
        412,415,1,0,0,0,413,411,1,0,0,0,413,414,1,0,0,0,414,73,1,0,0,0,415,
        413,1,0,0,0,416,417,7,3,0,0,417,75,1,0,0,0,418,424,3,80,40,0,419,
        420,3,78,39,0,420,421,3,80,40,0,421,423,1,0,0,0,422,419,1,0,0,0,
        423,426,1,0,0,0,424,422,1,0,0,0,424,425,1,0,0,0,425,77,1,0,0,0,426,
        424,1,0,0,0,427,428,7,4,0,0,428,79,1,0,0,0,429,430,7,5,0,0,430,435,
        3,80,40,0,431,432,7,6,0,0,432,435,3,80,40,0,433,435,3,82,41,0,434,
        429,1,0,0,0,434,431,1,0,0,0,434,433,1,0,0,0,435,81,1,0,0,0,436,458,
        3,84,42,0,437,438,5,93,0,0,438,439,5,97,0,0,439,440,5,94,0,0,440,
        442,5,87,0,0,441,443,3,90,45,0,442,441,1,0,0,0,442,443,1,0,0,0,443,
        444,1,0,0,0,444,457,5,88,0,0,445,447,5,87,0,0,446,448,3,90,45,0,
        447,446,1,0,0,0,447,448,1,0,0,0,448,449,1,0,0,0,449,457,5,88,0,0,
        450,451,5,51,0,0,451,457,5,97,0,0,452,453,5,89,0,0,453,454,3,60,
        30,0,454,455,5,90,0,0,455,457,1,0,0,0,456,437,1,0,0,0,456,445,1,
        0,0,0,456,450,1,0,0,0,456,452,1,0,0,0,457,460,1,0,0,0,458,456,1,
        0,0,0,458,459,1,0,0,0,459,83,1,0,0,0,460,458,1,0,0,0,461,480,5,95,
        0,0,462,480,5,96,0,0,463,480,5,53,0,0,464,480,5,54,0,0,465,480,5,
        55,0,0,466,480,5,97,0,0,467,468,5,87,0,0,468,469,3,60,30,0,469,470,
        5,88,0,0,470,480,1,0,0,0,471,473,5,89,0,0,472,474,3,90,45,0,473,
        472,1,0,0,0,473,474,1,0,0,0,474,475,1,0,0,0,475,480,5,90,0,0,476,
        477,5,93,0,0,477,478,5,97,0,0,478,480,5,94,0,0,479,461,1,0,0,0,479,
        462,1,0,0,0,479,463,1,0,0,0,479,464,1,0,0,0,479,465,1,0,0,0,479,
        466,1,0,0,0,479,467,1,0,0,0,479,471,1,0,0,0,479,476,1,0,0,0,480,
        85,1,0,0,0,481,484,3,88,44,0,482,484,5,97,0,0,483,481,1,0,0,0,483,
        482,1,0,0,0,484,87,1,0,0,0,485,486,7,7,0,0,486,89,1,0,0,0,487,492,
        3,60,30,0,488,489,5,83,0,0,489,491,3,60,30,0,490,488,1,0,0,0,491,
        494,1,0,0,0,492,490,1,0,0,0,492,493,1,0,0,0,493,91,1,0,0,0,494,492,
        1,0,0,0,60,97,99,111,119,124,130,137,143,147,152,163,167,173,183,
        187,194,199,201,208,211,218,226,233,247,253,256,262,269,276,286,
        292,296,303,307,318,324,328,332,335,339,343,354,359,364,368,377,
        385,393,402,413,424,434,442,447,456,458,473,479,483,492
    ]

class DuanLangParser ( Parser ):

    grammarFileName = "DuanLangParser.g4"

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    sharedContextCache = PredictionContextCache()

    literalNames = [ "<INVALID>", "<INVALID>", "<INVALID>", "'```'", "<INVALID>", 
                     "'\\u5426\\u5219\\u82E5'", "'\\u5982\\u679C'", "'\\u90A3\\u4E48'", 
                     "'\\u5426\\u5219'", "'\\u7ED3\\u675F'", "'\\u5927\\u4E8E\\u7B49\\u4E8E'", 
                     "'\\u5C0F\\u4E8E\\u7B49\\u4E8E'", "'\\u4E0D\\u7B49\\u4E8E'", 
                     "'\\u5927\\u4E8E'", "'\\u5C0F\\u4E8E'", "'\\u5B9A\\u4E49'", 
                     "'\\u7B49\\u4E8E'", "'\\u6BB5'", "'\\u6570\\u636E\\u7C7B\\u578B'", 
                     "'\\u9519\\u8BEF'", "'\\u5E38\\u91CF'", "'\\u7C7B\\u578B'", 
                     "'\\u5BFC\\u51FA'", "'\\u5BFC\\u5165'", "'\\u4ECE'", 
                     "'\\u904D\\u5386'", "'\\u5F53'", "'\\u8DF3\\u51FA'", 
                     "'\\u8DF3\\u8FC7'", "'\\u5C1D\\u8BD5'", "'\\u6355\\u83B7'", 
                     "'\\u629B\\u51FA'", "'\\u8FD4\\u56DE'", "'\\u6253\\u5370'", 
                     "'\\u8F93\\u51FA'", "'\\u8F93\\u5165'", "'\\u7EE7\\u627F'", 
                     "'\\u4F7F\\u7528'", "'\\u7236'", "'\\u81EA\\u6211'", 
                     "'\\u65B9\\u6CD5'", "'\\u4E14'", "'\\u6216'", "'\\u975E'", 
                     "'\\u52A0'", "'\\u51CF'", "'\\u4E58'", "'\\u9664'", 
                     "'\\u6A21'", "'\\u5E42'", "'\\u5E76'", "'\\u4E4B'", 
                     "'\\u7684'", "'\\u771F'", "'\\u5047'", "'\\u7A7A'", 
                     "'\\u6570'", "'\\u6574\\u6570'", "'\\u6D6E\\u6570'", 
                     "'\\u4E32'", "'\\u5217'", "'\\u5178'", "'\\u96C6'", 
                     "'\\u5E03\\u5C14'", "'\\u4EFB\\u610F'", "'^'", "'%'", 
                     "<INVALID>", "<INVALID>", "'+'", "'-'", "'=='", "'!='", 
                     "'>='", "'<='", "'>'", "'<'", "'!'", "'&&'", "'||'", 
                     "'->'", "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                     "<INVALID>", "'\\u3001'", "<INVALID>", "<INVALID>", 
                     "<INVALID>", "<INVALID>", "'{'", "'}'", "'\\u300A'", 
                     "'\\u300B'" ]

    symbolicNames = [ "<INVALID>", "LINE_COMMENT", "COMMENT_START", "COMMENT_CLOSE", 
                      "COMMENT_CONTENT", "K_ELSE_IF", "K_IF", "K_THEN", 
                      "K_ELSE", "K_END", "K_GE", "K_LE", "K_NE", "K_GT", 
                      "K_LT", "K_DEFINE", "K_EQUAL", "K_SEGMENT", "K_DATA_TYPE", 
                      "K_ERROR_TYPE", "K_CONST", "K_TYPE", "K_EXPORT", "K_IMPORT", 
                      "K_FROM", "K_FOREACH", "K_WHILE", "K_BREAK", "K_CONTINUE", 
                      "K_TRY", "K_CATCH", "K_THROW", "K_RETURN", "K_PRINT", 
                      "K_OUTPUT", "K_INPUT", "K_INHERIT", "K_USE", "K_PARENT", 
                      "K_SELF", "K_METHOD", "K_AND", "K_OR", "K_NOT", "K_PLUS", 
                      "K_MINUS", "K_MULTIPLY", "K_DIVIDE", "K_MOD", "K_POW", 
                      "K_AND_WORD", "K_OF", "K_DE", "K_TRUE", "K_FALSE", 
                      "K_NULL", "T_NUMBER", "T_INT", "T_FLOAT", "T_STRING", 
                      "T_LIST", "T_DICT", "T_SET", "T_BOOL", "T_ANY", "POW", 
                      "MODULO", "MULTIPLY", "DIVIDE", "PLUS", "MINUS", "EQ", 
                      "NE", "GE", "LE", "GT", "LT", "NOT", "AND", "OR", 
                      "PIPE", "PATH_SEP", "DOT", "COMMA", "COLON", "SEMICOLON", 
                      "PAUSE", "LPAREN", "RPAREN", "LBRACKET", "RBRACKET", 
                      "LBRACE", "RBRACE", "BOOK_L", "BOOK_R", "NUMBER", 
                      "STRING", "ID", "NEWLINE", "WS", "UNKNOWN" ]

    RULE_program = 0
    RULE_moduleDecl = 1
    RULE_definition = 2
    RULE_paragraphDef = 3
    RULE_paramList = 4
    RULE_param = 5
    RULE_block = 6
    RULE_dataTypeDef = 7
    RULE_dataTypeField = 8
    RULE_errorTypeDef = 9
    RULE_importStmt = 10
    RULE_exportStmt = 11
    RULE_path = 12
    RULE_importList = 13
    RULE_importItem = 14
    RULE_stmt = 15
    RULE_varDecl = 16
    RULE_assignStmt = 17
    RULE_target = 18
    RULE_ifStmt = 19
    RULE_foreachStmt = 20
    RULE_foreachVar = 21
    RULE_whileStmt = 22
    RULE_returnStmt = 23
    RULE_breakStmt = 24
    RULE_continueStmt = 25
    RULE_tryStmt = 26
    RULE_throwStmt = 27
    RULE_printStmt = 28
    RULE_exprStmt = 29
    RULE_expr = 30
    RULE_pipelineExpr = 31
    RULE_andExpr = 32
    RULE_orExpr = 33
    RULE_comparisonExpr = 34
    RULE_compOp = 35
    RULE_additiveExpr = 36
    RULE_addOp = 37
    RULE_multiplicativeExpr = 38
    RULE_multOp = 39
    RULE_unaryExpr = 40
    RULE_postfixExpr = 41
    RULE_primary = 42
    RULE_typeAnnotation = 43
    RULE_builtinType = 44
    RULE_exprList = 45

    ruleNames =  [ "program", "moduleDecl", "definition", "paragraphDef", 
                   "paramList", "param", "block", "dataTypeDef", "dataTypeField", 
                   "errorTypeDef", "importStmt", "exportStmt", "path", "importList", 
                   "importItem", "stmt", "varDecl", "assignStmt", "target", 
                   "ifStmt", "foreachStmt", "foreachVar", "whileStmt", "returnStmt", 
                   "breakStmt", "continueStmt", "tryStmt", "throwStmt", 
                   "printStmt", "exprStmt", "expr", "pipelineExpr", "andExpr", 
                   "orExpr", "comparisonExpr", "compOp", "additiveExpr", 
                   "addOp", "multiplicativeExpr", "multOp", "unaryExpr", 
                   "postfixExpr", "primary", "typeAnnotation", "builtinType", 
                   "exprList" ]

    EOF = Token.EOF
    LINE_COMMENT=1
    COMMENT_START=2
    COMMENT_CLOSE=3
    COMMENT_CONTENT=4
    K_ELSE_IF=5
    K_IF=6
    K_THEN=7
    K_ELSE=8
    K_END=9
    K_GE=10
    K_LE=11
    K_NE=12
    K_GT=13
    K_LT=14
    K_DEFINE=15
    K_EQUAL=16
    K_SEGMENT=17
    K_DATA_TYPE=18
    K_ERROR_TYPE=19
    K_CONST=20
    K_TYPE=21
    K_EXPORT=22
    K_IMPORT=23
    K_FROM=24
    K_FOREACH=25
    K_WHILE=26
    K_BREAK=27
    K_CONTINUE=28
    K_TRY=29
    K_CATCH=30
    K_THROW=31
    K_RETURN=32
    K_PRINT=33
    K_OUTPUT=34
    K_INPUT=35
    K_INHERIT=36
    K_USE=37
    K_PARENT=38
    K_SELF=39
    K_METHOD=40
    K_AND=41
    K_OR=42
    K_NOT=43
    K_PLUS=44
    K_MINUS=45
    K_MULTIPLY=46
    K_DIVIDE=47
    K_MOD=48
    K_POW=49
    K_AND_WORD=50
    K_OF=51
    K_DE=52
    K_TRUE=53
    K_FALSE=54
    K_NULL=55
    T_NUMBER=56
    T_INT=57
    T_FLOAT=58
    T_STRING=59
    T_LIST=60
    T_DICT=61
    T_SET=62
    T_BOOL=63
    T_ANY=64
    POW=65
    MODULO=66
    MULTIPLY=67
    DIVIDE=68
    PLUS=69
    MINUS=70
    EQ=71
    NE=72
    GE=73
    LE=74
    GT=75
    LT=76
    NOT=77
    AND=78
    OR=79
    PIPE=80
    PATH_SEP=81
    DOT=82
    COMMA=83
    COLON=84
    SEMICOLON=85
    PAUSE=86
    LPAREN=87
    RPAREN=88
    LBRACKET=89
    RBRACKET=90
    LBRACE=91
    RBRACE=92
    BOOK_L=93
    BOOK_R=94
    NUMBER=95
    STRING=96
    ID=97
    NEWLINE=98
    WS=99
    UNKNOWN=100

    def __init__(self, input:TokenStream, output:TextIO = sys.stdout):
        super().__init__(input, output)
        self.checkVersion("4.13.2")
        self._interp = ParserATNSimulator(self, self.atn, self.decisionsToDFA, self.sharedContextCache)
        self._predicates = None




    class ProgramContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def EOF(self):
            return self.getToken(DuanLangParser.EOF, 0)

        def moduleDecl(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(DuanLangParser.ModuleDeclContext)
            else:
                return self.getTypedRuleContext(DuanLangParser.ModuleDeclContext,i)


        def importStmt(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(DuanLangParser.ImportStmtContext)
            else:
                return self.getTypedRuleContext(DuanLangParser.ImportStmtContext,i)


        def exportStmt(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(DuanLangParser.ExportStmtContext)
            else:
                return self.getTypedRuleContext(DuanLangParser.ExportStmtContext,i)


        def definition(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(DuanLangParser.DefinitionContext)
            else:
                return self.getTypedRuleContext(DuanLangParser.DefinitionContext,i)


        def stmt(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(DuanLangParser.StmtContext)
            else:
                return self.getTypedRuleContext(DuanLangParser.StmtContext,i)


        def getRuleIndex(self):
            return DuanLangParser.RULE_program

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitProgram" ):
                return visitor.visitProgram(self)
            else:
                return visitor.visitChildren(self)




    def program(self):

        localctx = DuanLangParser.ProgramContext(self, self._ctx, self.state)
        self.enterRule(localctx, 0, self.RULE_program)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 99
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while (((_la) & ~0x3f) == 0 and ((1 << _la) & 63094408530133056) != 0) or ((((_la - 70)) & ~0x3f) == 0 and ((1 << (_la - 70)) & 243925121) != 0):
                self.state = 97
                self._errHandler.sync(self)
                la_ = self._interp.adaptivePredict(self._input,0,self._ctx)
                if la_ == 1:
                    self.state = 92
                    self.moduleDecl()
                    pass

                elif la_ == 2:
                    self.state = 93
                    self.importStmt()
                    pass

                elif la_ == 3:
                    self.state = 94
                    self.exportStmt()
                    pass

                elif la_ == 4:
                    self.state = 95
                    self.definition()
                    pass

                elif la_ == 5:
                    self.state = 96
                    self.stmt()
                    pass


                self.state = 101
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 102
            self.match(DuanLangParser.EOF)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ModuleDeclContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def LBRACKET(self):
            return self.getToken(DuanLangParser.LBRACKET, 0)

        def ID(self):
            return self.getToken(DuanLangParser.ID, 0)

        def RBRACKET(self):
            return self.getToken(DuanLangParser.RBRACKET, 0)

        def getRuleIndex(self):
            return DuanLangParser.RULE_moduleDecl

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitModuleDecl" ):
                return visitor.visitModuleDecl(self)
            else:
                return visitor.visitChildren(self)




    def moduleDecl(self):

        localctx = DuanLangParser.ModuleDeclContext(self, self._ctx, self.state)
        self.enterRule(localctx, 2, self.RULE_moduleDecl)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 104
            self.match(DuanLangParser.LBRACKET)
            self.state = 105
            self.match(DuanLangParser.ID)
            self.state = 106
            self.match(DuanLangParser.RBRACKET)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class DefinitionContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def paragraphDef(self):
            return self.getTypedRuleContext(DuanLangParser.ParagraphDefContext,0)


        def dataTypeDef(self):
            return self.getTypedRuleContext(DuanLangParser.DataTypeDefContext,0)


        def errorTypeDef(self):
            return self.getTypedRuleContext(DuanLangParser.ErrorTypeDefContext,0)


        def getRuleIndex(self):
            return DuanLangParser.RULE_definition

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitDefinition" ):
                return visitor.visitDefinition(self)
            else:
                return visitor.visitChildren(self)




    def definition(self):

        localctx = DuanLangParser.DefinitionContext(self, self._ctx, self.state)
        self.enterRule(localctx, 4, self.RULE_definition)
        try:
            self.state = 111
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,2,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 108
                self.paragraphDef()
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 109
                self.dataTypeDef()
                pass

            elif la_ == 3:
                self.enterOuterAlt(localctx, 3)
                self.state = 110
                self.errorTypeDef()
                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ParagraphDefContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def BOOK_L(self):
            return self.getToken(DuanLangParser.BOOK_L, 0)

        def ID(self):
            return self.getToken(DuanLangParser.ID, 0)

        def BOOK_R(self):
            return self.getToken(DuanLangParser.BOOK_R, 0)

        def K_SEGMENT(self):
            return self.getToken(DuanLangParser.K_SEGMENT, 0)

        def LPAREN(self):
            return self.getToken(DuanLangParser.LPAREN, 0)

        def RPAREN(self):
            return self.getToken(DuanLangParser.RPAREN, 0)

        def COLON(self):
            return self.getToken(DuanLangParser.COLON, 0)

        def block(self):
            return self.getTypedRuleContext(DuanLangParser.BlockContext,0)


        def K_END(self):
            return self.getToken(DuanLangParser.K_END, 0)

        def paramList(self):
            return self.getTypedRuleContext(DuanLangParser.ParamListContext,0)


        def PIPE(self):
            return self.getToken(DuanLangParser.PIPE, 0)

        def typeAnnotation(self):
            return self.getTypedRuleContext(DuanLangParser.TypeAnnotationContext,0)


        def DOT(self):
            return self.getToken(DuanLangParser.DOT, 0)

        def getRuleIndex(self):
            return DuanLangParser.RULE_paragraphDef

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitParagraphDef" ):
                return visitor.visitParagraphDef(self)
            else:
                return visitor.visitChildren(self)




    def paragraphDef(self):

        localctx = DuanLangParser.ParagraphDefContext(self, self._ctx, self.state)
        self.enterRule(localctx, 6, self.RULE_paragraphDef)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 113
            self.match(DuanLangParser.BOOK_L)
            self.state = 114
            self.match(DuanLangParser.ID)
            self.state = 115
            self.match(DuanLangParser.BOOK_R)
            self.state = 116
            self.match(DuanLangParser.K_SEGMENT)
            self.state = 117
            self.match(DuanLangParser.LPAREN)
            self.state = 119
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==97:
                self.state = 118
                self.paramList()


            self.state = 121
            self.match(DuanLangParser.RPAREN)
            self.state = 124
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==80:
                self.state = 122
                self.match(DuanLangParser.PIPE)
                self.state = 123
                self.typeAnnotation()


            self.state = 126
            self.match(DuanLangParser.COLON)
            self.state = 127
            self.block()
            self.state = 128
            self.match(DuanLangParser.K_END)
            self.state = 130
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==82:
                self.state = 129
                self.match(DuanLangParser.DOT)


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ParamListContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def param(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(DuanLangParser.ParamContext)
            else:
                return self.getTypedRuleContext(DuanLangParser.ParamContext,i)


        def COMMA(self, i:int=None):
            if i is None:
                return self.getTokens(DuanLangParser.COMMA)
            else:
                return self.getToken(DuanLangParser.COMMA, i)

        def getRuleIndex(self):
            return DuanLangParser.RULE_paramList

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitParamList" ):
                return visitor.visitParamList(self)
            else:
                return visitor.visitChildren(self)




    def paramList(self):

        localctx = DuanLangParser.ParamListContext(self, self._ctx, self.state)
        self.enterRule(localctx, 8, self.RULE_paramList)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 132
            self.param()
            self.state = 137
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==83:
                self.state = 133
                self.match(DuanLangParser.COMMA)
                self.state = 134
                self.param()
                self.state = 139
                self._errHandler.sync(self)
                _la = self._input.LA(1)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ParamContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def ID(self):
            return self.getToken(DuanLangParser.ID, 0)

        def COLON(self):
            return self.getToken(DuanLangParser.COLON, 0)

        def typeAnnotation(self):
            return self.getTypedRuleContext(DuanLangParser.TypeAnnotationContext,0)


        def K_EQUAL(self):
            return self.getToken(DuanLangParser.K_EQUAL, 0)

        def expr(self):
            return self.getTypedRuleContext(DuanLangParser.ExprContext,0)


        def getRuleIndex(self):
            return DuanLangParser.RULE_param

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitParam" ):
                return visitor.visitParam(self)
            else:
                return visitor.visitChildren(self)




    def param(self):

        localctx = DuanLangParser.ParamContext(self, self._ctx, self.state)
        self.enterRule(localctx, 10, self.RULE_param)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 140
            self.match(DuanLangParser.ID)
            self.state = 143
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==84:
                self.state = 141
                self.match(DuanLangParser.COLON)
                self.state = 142
                self.typeAnnotation()


            self.state = 147
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==16:
                self.state = 145
                self.match(DuanLangParser.K_EQUAL)
                self.state = 146
                self.expr()


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class BlockContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def stmt(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(DuanLangParser.StmtContext)
            else:
                return self.getTypedRuleContext(DuanLangParser.StmtContext,i)


        def getRuleIndex(self):
            return DuanLangParser.RULE_block

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitBlock" ):
                return visitor.visitBlock(self)
            else:
                return visitor.visitChildren(self)




    def block(self):

        localctx = DuanLangParser.BlockContext(self, self._ctx, self.state)
        self.enterRule(localctx, 12, self.RULE_block)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 152
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while (((_la) & ~0x3f) == 0 and ((1 << _la) & 63094408500772928) != 0) or ((((_la - 70)) & ~0x3f) == 0 and ((1 << (_la - 70)) & 243925121) != 0):
                self.state = 149
                self.stmt()
                self.state = 154
                self._errHandler.sync(self)
                _la = self._input.LA(1)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class DataTypeDefContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def BOOK_L(self):
            return self.getToken(DuanLangParser.BOOK_L, 0)

        def ID(self):
            return self.getToken(DuanLangParser.ID, 0)

        def BOOK_R(self):
            return self.getToken(DuanLangParser.BOOK_R, 0)

        def K_DATA_TYPE(self):
            return self.getToken(DuanLangParser.K_DATA_TYPE, 0)

        def COLON(self):
            return self.getToken(DuanLangParser.COLON, 0)

        def K_END(self):
            return self.getToken(DuanLangParser.K_END, 0)

        def dataTypeField(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(DuanLangParser.DataTypeFieldContext)
            else:
                return self.getTypedRuleContext(DuanLangParser.DataTypeFieldContext,i)


        def DOT(self):
            return self.getToken(DuanLangParser.DOT, 0)

        def getRuleIndex(self):
            return DuanLangParser.RULE_dataTypeDef

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitDataTypeDef" ):
                return visitor.visitDataTypeDef(self)
            else:
                return visitor.visitChildren(self)




    def dataTypeDef(self):

        localctx = DuanLangParser.DataTypeDefContext(self, self._ctx, self.state)
        self.enterRule(localctx, 14, self.RULE_dataTypeDef)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 155
            self.match(DuanLangParser.BOOK_L)
            self.state = 156
            self.match(DuanLangParser.ID)
            self.state = 157
            self.match(DuanLangParser.BOOK_R)
            self.state = 158
            self.match(DuanLangParser.K_DATA_TYPE)
            self.state = 159
            self.match(DuanLangParser.COLON)
            self.state = 161 
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while True:
                self.state = 160
                self.dataTypeField()
                self.state = 163 
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if not (_la==97):
                    break

            self.state = 165
            self.match(DuanLangParser.K_END)
            self.state = 167
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==82:
                self.state = 166
                self.match(DuanLangParser.DOT)


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class DataTypeFieldContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def ID(self):
            return self.getToken(DuanLangParser.ID, 0)

        def COLON(self):
            return self.getToken(DuanLangParser.COLON, 0)

        def typeAnnotation(self):
            return self.getTypedRuleContext(DuanLangParser.TypeAnnotationContext,0)


        def DOT(self):
            return self.getToken(DuanLangParser.DOT, 0)

        def getRuleIndex(self):
            return DuanLangParser.RULE_dataTypeField

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitDataTypeField" ):
                return visitor.visitDataTypeField(self)
            else:
                return visitor.visitChildren(self)




    def dataTypeField(self):

        localctx = DuanLangParser.DataTypeFieldContext(self, self._ctx, self.state)
        self.enterRule(localctx, 16, self.RULE_dataTypeField)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 169
            self.match(DuanLangParser.ID)
            self.state = 170
            self.match(DuanLangParser.COLON)
            self.state = 171
            self.typeAnnotation()
            self.state = 173
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==82:
                self.state = 172
                self.match(DuanLangParser.DOT)


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ErrorTypeDefContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def BOOK_L(self):
            return self.getToken(DuanLangParser.BOOK_L, 0)

        def ID(self):
            return self.getToken(DuanLangParser.ID, 0)

        def BOOK_R(self):
            return self.getToken(DuanLangParser.BOOK_R, 0)

        def K_ERROR_TYPE(self):
            return self.getToken(DuanLangParser.K_ERROR_TYPE, 0)

        def COLON(self):
            return self.getToken(DuanLangParser.COLON, 0)

        def K_END(self):
            return self.getToken(DuanLangParser.K_END, 0)

        def dataTypeField(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(DuanLangParser.DataTypeFieldContext)
            else:
                return self.getTypedRuleContext(DuanLangParser.DataTypeFieldContext,i)


        def DOT(self):
            return self.getToken(DuanLangParser.DOT, 0)

        def getRuleIndex(self):
            return DuanLangParser.RULE_errorTypeDef

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitErrorTypeDef" ):
                return visitor.visitErrorTypeDef(self)
            else:
                return visitor.visitChildren(self)




    def errorTypeDef(self):

        localctx = DuanLangParser.ErrorTypeDefContext(self, self._ctx, self.state)
        self.enterRule(localctx, 18, self.RULE_errorTypeDef)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 175
            self.match(DuanLangParser.BOOK_L)
            self.state = 176
            self.match(DuanLangParser.ID)
            self.state = 177
            self.match(DuanLangParser.BOOK_R)
            self.state = 178
            self.match(DuanLangParser.K_ERROR_TYPE)
            self.state = 179
            self.match(DuanLangParser.COLON)
            self.state = 181 
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while True:
                self.state = 180
                self.dataTypeField()
                self.state = 183 
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if not (_la==97):
                    break

            self.state = 185
            self.match(DuanLangParser.K_END)
            self.state = 187
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==82:
                self.state = 186
                self.match(DuanLangParser.DOT)


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ImportStmtContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def K_FROM(self):
            return self.getToken(DuanLangParser.K_FROM, 0)

        def path(self):
            return self.getTypedRuleContext(DuanLangParser.PathContext,0)


        def K_IMPORT(self):
            return self.getToken(DuanLangParser.K_IMPORT, 0)

        def importList(self):
            return self.getTypedRuleContext(DuanLangParser.ImportListContext,0)


        def DOT(self):
            return self.getToken(DuanLangParser.DOT, 0)

        def getRuleIndex(self):
            return DuanLangParser.RULE_importStmt

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitImportStmt" ):
                return visitor.visitImportStmt(self)
            else:
                return visitor.visitChildren(self)




    def importStmt(self):

        localctx = DuanLangParser.ImportStmtContext(self, self._ctx, self.state)
        self.enterRule(localctx, 20, self.RULE_importStmt)
        self._la = 0 # Token type
        try:
            self.state = 201
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [24]:
                self.enterOuterAlt(localctx, 1)
                self.state = 189
                self.match(DuanLangParser.K_FROM)
                self.state = 190
                self.path()
                self.state = 191
                self.match(DuanLangParser.K_IMPORT)
                self.state = 192
                self.importList()
                self.state = 194
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la==82:
                    self.state = 193
                    self.match(DuanLangParser.DOT)


                pass
            elif token in [23]:
                self.enterOuterAlt(localctx, 2)
                self.state = 196
                self.match(DuanLangParser.K_IMPORT)
                self.state = 197
                self.importList()
                self.state = 199
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la==82:
                    self.state = 198
                    self.match(DuanLangParser.DOT)


                pass
            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ExportStmtContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def K_EXPORT(self):
            return self.getToken(DuanLangParser.K_EXPORT, 0)

        def ID(self):
            return self.getToken(DuanLangParser.ID, 0)

        def BOOK_L(self):
            return self.getToken(DuanLangParser.BOOK_L, 0)

        def BOOK_R(self):
            return self.getToken(DuanLangParser.BOOK_R, 0)

        def DOT(self):
            return self.getToken(DuanLangParser.DOT, 0)

        def getRuleIndex(self):
            return DuanLangParser.RULE_exportStmt

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitExportStmt" ):
                return visitor.visitExportStmt(self)
            else:
                return visitor.visitChildren(self)




    def exportStmt(self):

        localctx = DuanLangParser.ExportStmtContext(self, self._ctx, self.state)
        self.enterRule(localctx, 22, self.RULE_exportStmt)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 203
            self.match(DuanLangParser.K_EXPORT)
            self.state = 208
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [97]:
                self.state = 204
                self.match(DuanLangParser.ID)
                pass
            elif token in [93]:
                self.state = 205
                self.match(DuanLangParser.BOOK_L)
                self.state = 206
                self.match(DuanLangParser.ID)
                self.state = 207
                self.match(DuanLangParser.BOOK_R)
                pass
            else:
                raise NoViableAltException(self)

            self.state = 211
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==82:
                self.state = 210
                self.match(DuanLangParser.DOT)


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class PathContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def ID(self, i:int=None):
            if i is None:
                return self.getTokens(DuanLangParser.ID)
            else:
                return self.getToken(DuanLangParser.ID, i)

        def PATH_SEP(self, i:int=None):
            if i is None:
                return self.getTokens(DuanLangParser.PATH_SEP)
            else:
                return self.getToken(DuanLangParser.PATH_SEP, i)

        def getRuleIndex(self):
            return DuanLangParser.RULE_path

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitPath" ):
                return visitor.visitPath(self)
            else:
                return visitor.visitChildren(self)




    def path(self):

        localctx = DuanLangParser.PathContext(self, self._ctx, self.state)
        self.enterRule(localctx, 24, self.RULE_path)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 213
            self.match(DuanLangParser.ID)
            self.state = 218
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==81:
                self.state = 214
                self.match(DuanLangParser.PATH_SEP)
                self.state = 215
                self.match(DuanLangParser.ID)
                self.state = 220
                self._errHandler.sync(self)
                _la = self._input.LA(1)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ImportListContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def importItem(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(DuanLangParser.ImportItemContext)
            else:
                return self.getTypedRuleContext(DuanLangParser.ImportItemContext,i)


        def COMMA(self, i:int=None):
            if i is None:
                return self.getTokens(DuanLangParser.COMMA)
            else:
                return self.getToken(DuanLangParser.COMMA, i)

        def getRuleIndex(self):
            return DuanLangParser.RULE_importList

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitImportList" ):
                return visitor.visitImportList(self)
            else:
                return visitor.visitChildren(self)




    def importList(self):

        localctx = DuanLangParser.ImportListContext(self, self._ctx, self.state)
        self.enterRule(localctx, 26, self.RULE_importList)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 221
            self.importItem()
            self.state = 226
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==83:
                self.state = 222
                self.match(DuanLangParser.COMMA)
                self.state = 223
                self.importItem()
                self.state = 228
                self._errHandler.sync(self)
                _la = self._input.LA(1)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ImportItemContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def BOOK_L(self):
            return self.getToken(DuanLangParser.BOOK_L, 0)

        def ID(self):
            return self.getToken(DuanLangParser.ID, 0)

        def BOOK_R(self):
            return self.getToken(DuanLangParser.BOOK_R, 0)

        def getRuleIndex(self):
            return DuanLangParser.RULE_importItem

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitImportItem" ):
                return visitor.visitImportItem(self)
            else:
                return visitor.visitChildren(self)




    def importItem(self):

        localctx = DuanLangParser.ImportItemContext(self, self._ctx, self.state)
        self.enterRule(localctx, 28, self.RULE_importItem)
        try:
            self.state = 233
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [93]:
                self.enterOuterAlt(localctx, 1)
                self.state = 229
                self.match(DuanLangParser.BOOK_L)
                self.state = 230
                self.match(DuanLangParser.ID)
                self.state = 231
                self.match(DuanLangParser.BOOK_R)
                pass
            elif token in [97]:
                self.enterOuterAlt(localctx, 2)
                self.state = 232
                self.match(DuanLangParser.ID)
                pass
            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class StmtContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def varDecl(self):
            return self.getTypedRuleContext(DuanLangParser.VarDeclContext,0)


        def assignStmt(self):
            return self.getTypedRuleContext(DuanLangParser.AssignStmtContext,0)


        def ifStmt(self):
            return self.getTypedRuleContext(DuanLangParser.IfStmtContext,0)


        def foreachStmt(self):
            return self.getTypedRuleContext(DuanLangParser.ForeachStmtContext,0)


        def whileStmt(self):
            return self.getTypedRuleContext(DuanLangParser.WhileStmtContext,0)


        def returnStmt(self):
            return self.getTypedRuleContext(DuanLangParser.ReturnStmtContext,0)


        def breakStmt(self):
            return self.getTypedRuleContext(DuanLangParser.BreakStmtContext,0)


        def continueStmt(self):
            return self.getTypedRuleContext(DuanLangParser.ContinueStmtContext,0)


        def tryStmt(self):
            return self.getTypedRuleContext(DuanLangParser.TryStmtContext,0)


        def throwStmt(self):
            return self.getTypedRuleContext(DuanLangParser.ThrowStmtContext,0)


        def printStmt(self):
            return self.getTypedRuleContext(DuanLangParser.PrintStmtContext,0)


        def exprStmt(self):
            return self.getTypedRuleContext(DuanLangParser.ExprStmtContext,0)


        def getRuleIndex(self):
            return DuanLangParser.RULE_stmt

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitStmt" ):
                return visitor.visitStmt(self)
            else:
                return visitor.visitChildren(self)




    def stmt(self):

        localctx = DuanLangParser.StmtContext(self, self._ctx, self.state)
        self.enterRule(localctx, 30, self.RULE_stmt)
        try:
            self.state = 247
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,23,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 235
                self.varDecl()
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 236
                self.assignStmt()
                pass

            elif la_ == 3:
                self.enterOuterAlt(localctx, 3)
                self.state = 237
                self.ifStmt()
                pass

            elif la_ == 4:
                self.enterOuterAlt(localctx, 4)
                self.state = 238
                self.foreachStmt()
                pass

            elif la_ == 5:
                self.enterOuterAlt(localctx, 5)
                self.state = 239
                self.whileStmt()
                pass

            elif la_ == 6:
                self.enterOuterAlt(localctx, 6)
                self.state = 240
                self.returnStmt()
                pass

            elif la_ == 7:
                self.enterOuterAlt(localctx, 7)
                self.state = 241
                self.breakStmt()
                pass

            elif la_ == 8:
                self.enterOuterAlt(localctx, 8)
                self.state = 242
                self.continueStmt()
                pass

            elif la_ == 9:
                self.enterOuterAlt(localctx, 9)
                self.state = 243
                self.tryStmt()
                pass

            elif la_ == 10:
                self.enterOuterAlt(localctx, 10)
                self.state = 244
                self.throwStmt()
                pass

            elif la_ == 11:
                self.enterOuterAlt(localctx, 11)
                self.state = 245
                self.printStmt()
                pass

            elif la_ == 12:
                self.enterOuterAlt(localctx, 12)
                self.state = 246
                self.exprStmt()
                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class VarDeclContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def K_DEFINE(self):
            return self.getToken(DuanLangParser.K_DEFINE, 0)

        def ID(self):
            return self.getToken(DuanLangParser.ID, 0)

        def K_EQUAL(self):
            return self.getToken(DuanLangParser.K_EQUAL, 0)

        def expr(self):
            return self.getTypedRuleContext(DuanLangParser.ExprContext,0)


        def DOT(self):
            return self.getToken(DuanLangParser.DOT, 0)

        def getRuleIndex(self):
            return DuanLangParser.RULE_varDecl

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitVarDecl" ):
                return visitor.visitVarDecl(self)
            else:
                return visitor.visitChildren(self)




    def varDecl(self):

        localctx = DuanLangParser.VarDeclContext(self, self._ctx, self.state)
        self.enterRule(localctx, 32, self.RULE_varDecl)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 249
            self.match(DuanLangParser.K_DEFINE)
            self.state = 250
            self.match(DuanLangParser.ID)
            self.state = 253
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==16:
                self.state = 251
                self.match(DuanLangParser.K_EQUAL)
                self.state = 252
                self.expr()


            self.state = 256
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==82:
                self.state = 255
                self.match(DuanLangParser.DOT)


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class AssignStmtContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def target(self):
            return self.getTypedRuleContext(DuanLangParser.TargetContext,0)


        def K_EQUAL(self):
            return self.getToken(DuanLangParser.K_EQUAL, 0)

        def expr(self):
            return self.getTypedRuleContext(DuanLangParser.ExprContext,0)


        def DOT(self):
            return self.getToken(DuanLangParser.DOT, 0)

        def getRuleIndex(self):
            return DuanLangParser.RULE_assignStmt

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitAssignStmt" ):
                return visitor.visitAssignStmt(self)
            else:
                return visitor.visitChildren(self)




    def assignStmt(self):

        localctx = DuanLangParser.AssignStmtContext(self, self._ctx, self.state)
        self.enterRule(localctx, 34, self.RULE_assignStmt)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 258
            self.target()
            self.state = 259
            self.match(DuanLangParser.K_EQUAL)
            self.state = 260
            self.expr()
            self.state = 262
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==82:
                self.state = 261
                self.match(DuanLangParser.DOT)


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class TargetContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def ID(self):
            return self.getToken(DuanLangParser.ID, 0)

        def expr(self):
            return self.getTypedRuleContext(DuanLangParser.ExprContext,0)


        def K_OF(self):
            return self.getToken(DuanLangParser.K_OF, 0)

        def getRuleIndex(self):
            return DuanLangParser.RULE_target

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitTarget" ):
                return visitor.visitTarget(self)
            else:
                return visitor.visitChildren(self)




    def target(self):

        localctx = DuanLangParser.TargetContext(self, self._ctx, self.state)
        self.enterRule(localctx, 36, self.RULE_target)
        try:
            self.state = 269
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,27,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 264
                self.match(DuanLangParser.ID)
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 265
                self.expr()
                self.state = 266
                self.match(DuanLangParser.K_OF)
                self.state = 267
                self.match(DuanLangParser.ID)
                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class IfStmtContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def K_IF(self):
            return self.getToken(DuanLangParser.K_IF, 0)

        def expr(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(DuanLangParser.ExprContext)
            else:
                return self.getTypedRuleContext(DuanLangParser.ExprContext,i)


        def K_THEN(self, i:int=None):
            if i is None:
                return self.getTokens(DuanLangParser.K_THEN)
            else:
                return self.getToken(DuanLangParser.K_THEN, i)

        def K_END(self):
            return self.getToken(DuanLangParser.K_END, 0)

        def COLON(self, i:int=None):
            if i is None:
                return self.getTokens(DuanLangParser.COLON)
            else:
                return self.getToken(DuanLangParser.COLON, i)

        def block(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(DuanLangParser.BlockContext)
            else:
                return self.getTypedRuleContext(DuanLangParser.BlockContext,i)


        def K_ELSE_IF(self, i:int=None):
            if i is None:
                return self.getTokens(DuanLangParser.K_ELSE_IF)
            else:
                return self.getToken(DuanLangParser.K_ELSE_IF, i)

        def K_ELSE(self):
            return self.getToken(DuanLangParser.K_ELSE, 0)

        def DOT(self):
            return self.getToken(DuanLangParser.DOT, 0)

        def getRuleIndex(self):
            return DuanLangParser.RULE_ifStmt

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitIfStmt" ):
                return visitor.visitIfStmt(self)
            else:
                return visitor.visitChildren(self)




    def ifStmt(self):

        localctx = DuanLangParser.IfStmtContext(self, self._ctx, self.state)
        self.enterRule(localctx, 38, self.RULE_ifStmt)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 271
            self.match(DuanLangParser.K_IF)
            self.state = 272
            self.expr()
            self.state = 273
            self.match(DuanLangParser.K_THEN)
            self.state = 276
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==84:
                self.state = 274
                self.match(DuanLangParser.COLON)
                self.state = 275
                self.block()


            self.state = 286
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==5:
                self.state = 278
                self.match(DuanLangParser.K_ELSE_IF)
                self.state = 279
                self.expr()
                self.state = 280
                self.match(DuanLangParser.K_THEN)
                self.state = 281
                self.match(DuanLangParser.COLON)
                self.state = 282
                self.block()
                self.state = 288
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 292
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==8:
                self.state = 289
                self.match(DuanLangParser.K_ELSE)
                self.state = 290
                self.match(DuanLangParser.COLON)
                self.state = 291
                self.block()


            self.state = 294
            self.match(DuanLangParser.K_END)
            self.state = 296
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==82:
                self.state = 295
                self.match(DuanLangParser.DOT)


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ForeachStmtContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def K_FOREACH(self):
            return self.getToken(DuanLangParser.K_FOREACH, 0)

        def foreachVar(self):
            return self.getTypedRuleContext(DuanLangParser.ForeachVarContext,0)


        def expr(self):
            return self.getTypedRuleContext(DuanLangParser.ExprContext,0)


        def K_END(self):
            return self.getToken(DuanLangParser.K_END, 0)

        def COLON(self):
            return self.getToken(DuanLangParser.COLON, 0)

        def block(self):
            return self.getTypedRuleContext(DuanLangParser.BlockContext,0)


        def DOT(self):
            return self.getToken(DuanLangParser.DOT, 0)

        def getRuleIndex(self):
            return DuanLangParser.RULE_foreachStmt

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitForeachStmt" ):
                return visitor.visitForeachStmt(self)
            else:
                return visitor.visitChildren(self)




    def foreachStmt(self):

        localctx = DuanLangParser.ForeachStmtContext(self, self._ctx, self.state)
        self.enterRule(localctx, 40, self.RULE_foreachStmt)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 298
            self.match(DuanLangParser.K_FOREACH)
            self.state = 299
            self.foreachVar()
            self.state = 300
            self.expr()
            self.state = 303
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==84:
                self.state = 301
                self.match(DuanLangParser.COLON)
                self.state = 302
                self.block()


            self.state = 305
            self.match(DuanLangParser.K_END)
            self.state = 307
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==82:
                self.state = 306
                self.match(DuanLangParser.DOT)


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ForeachVarContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def ID(self, i:int=None):
            if i is None:
                return self.getTokens(DuanLangParser.ID)
            else:
                return self.getToken(DuanLangParser.ID, i)

        def K_OF(self):
            return self.getToken(DuanLangParser.K_OF, 0)

        def COMMA(self):
            return self.getToken(DuanLangParser.COMMA, 0)

        def getRuleIndex(self):
            return DuanLangParser.RULE_foreachVar

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitForeachVar" ):
                return visitor.visitForeachVar(self)
            else:
                return visitor.visitChildren(self)




    def foreachVar(self):

        localctx = DuanLangParser.ForeachVarContext(self, self._ctx, self.state)
        self.enterRule(localctx, 42, self.RULE_foreachVar)
        try:
            self.state = 318
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,34,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 309
                self.match(DuanLangParser.ID)
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 310
                self.match(DuanLangParser.ID)
                self.state = 311
                self.match(DuanLangParser.K_OF)
                self.state = 312
                self.match(DuanLangParser.ID)
                pass

            elif la_ == 3:
                self.enterOuterAlt(localctx, 3)
                self.state = 313
                self.match(DuanLangParser.ID)
                self.state = 314
                self.match(DuanLangParser.K_OF)
                self.state = 315
                self.match(DuanLangParser.ID)
                self.state = 316
                self.match(DuanLangParser.COMMA)
                self.state = 317
                self.match(DuanLangParser.ID)
                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class WhileStmtContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def K_WHILE(self):
            return self.getToken(DuanLangParser.K_WHILE, 0)

        def expr(self):
            return self.getTypedRuleContext(DuanLangParser.ExprContext,0)


        def K_END(self):
            return self.getToken(DuanLangParser.K_END, 0)

        def COLON(self):
            return self.getToken(DuanLangParser.COLON, 0)

        def block(self):
            return self.getTypedRuleContext(DuanLangParser.BlockContext,0)


        def DOT(self):
            return self.getToken(DuanLangParser.DOT, 0)

        def getRuleIndex(self):
            return DuanLangParser.RULE_whileStmt

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitWhileStmt" ):
                return visitor.visitWhileStmt(self)
            else:
                return visitor.visitChildren(self)




    def whileStmt(self):

        localctx = DuanLangParser.WhileStmtContext(self, self._ctx, self.state)
        self.enterRule(localctx, 44, self.RULE_whileStmt)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 320
            self.match(DuanLangParser.K_WHILE)
            self.state = 321
            self.expr()
            self.state = 324
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==84:
                self.state = 322
                self.match(DuanLangParser.COLON)
                self.state = 323
                self.block()


            self.state = 326
            self.match(DuanLangParser.K_END)
            self.state = 328
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==82:
                self.state = 327
                self.match(DuanLangParser.DOT)


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ReturnStmtContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def K_RETURN(self):
            return self.getToken(DuanLangParser.K_RETURN, 0)

        def expr(self):
            return self.getTypedRuleContext(DuanLangParser.ExprContext,0)


        def DOT(self):
            return self.getToken(DuanLangParser.DOT, 0)

        def getRuleIndex(self):
            return DuanLangParser.RULE_returnStmt

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitReturnStmt" ):
                return visitor.visitReturnStmt(self)
            else:
                return visitor.visitChildren(self)




    def returnStmt(self):

        localctx = DuanLangParser.ReturnStmtContext(self, self._ctx, self.state)
        self.enterRule(localctx, 46, self.RULE_returnStmt)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 330
            self.match(DuanLangParser.K_RETURN)
            self.state = 332
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,37,self._ctx)
            if la_ == 1:
                self.state = 331
                self.expr()


            self.state = 335
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==82:
                self.state = 334
                self.match(DuanLangParser.DOT)


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class BreakStmtContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def K_BREAK(self):
            return self.getToken(DuanLangParser.K_BREAK, 0)

        def DOT(self):
            return self.getToken(DuanLangParser.DOT, 0)

        def getRuleIndex(self):
            return DuanLangParser.RULE_breakStmt

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitBreakStmt" ):
                return visitor.visitBreakStmt(self)
            else:
                return visitor.visitChildren(self)




    def breakStmt(self):

        localctx = DuanLangParser.BreakStmtContext(self, self._ctx, self.state)
        self.enterRule(localctx, 48, self.RULE_breakStmt)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 337
            self.match(DuanLangParser.K_BREAK)
            self.state = 339
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==82:
                self.state = 338
                self.match(DuanLangParser.DOT)


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ContinueStmtContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def K_CONTINUE(self):
            return self.getToken(DuanLangParser.K_CONTINUE, 0)

        def DOT(self):
            return self.getToken(DuanLangParser.DOT, 0)

        def getRuleIndex(self):
            return DuanLangParser.RULE_continueStmt

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitContinueStmt" ):
                return visitor.visitContinueStmt(self)
            else:
                return visitor.visitChildren(self)




    def continueStmt(self):

        localctx = DuanLangParser.ContinueStmtContext(self, self._ctx, self.state)
        self.enterRule(localctx, 50, self.RULE_continueStmt)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 341
            self.match(DuanLangParser.K_CONTINUE)
            self.state = 343
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==82:
                self.state = 342
                self.match(DuanLangParser.DOT)


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class TryStmtContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def K_TRY(self):
            return self.getToken(DuanLangParser.K_TRY, 0)

        def COLON(self, i:int=None):
            if i is None:
                return self.getTokens(DuanLangParser.COLON)
            else:
                return self.getToken(DuanLangParser.COLON, i)

        def block(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(DuanLangParser.BlockContext)
            else:
                return self.getTypedRuleContext(DuanLangParser.BlockContext,i)


        def K_CATCH(self):
            return self.getToken(DuanLangParser.K_CATCH, 0)

        def ID(self):
            return self.getToken(DuanLangParser.ID, 0)

        def K_END(self):
            return self.getToken(DuanLangParser.K_END, 0)

        def DOT(self):
            return self.getToken(DuanLangParser.DOT, 0)

        def getRuleIndex(self):
            return DuanLangParser.RULE_tryStmt

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitTryStmt" ):
                return visitor.visitTryStmt(self)
            else:
                return visitor.visitChildren(self)




    def tryStmt(self):

        localctx = DuanLangParser.TryStmtContext(self, self._ctx, self.state)
        self.enterRule(localctx, 52, self.RULE_tryStmt)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 345
            self.match(DuanLangParser.K_TRY)
            self.state = 346
            self.match(DuanLangParser.COLON)
            self.state = 347
            self.block()
            self.state = 348
            self.match(DuanLangParser.K_CATCH)
            self.state = 349
            self.match(DuanLangParser.ID)
            self.state = 350
            self.match(DuanLangParser.COLON)
            self.state = 351
            self.block()
            self.state = 352
            self.match(DuanLangParser.K_END)
            self.state = 354
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==82:
                self.state = 353
                self.match(DuanLangParser.DOT)


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ThrowStmtContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def K_THROW(self):
            return self.getToken(DuanLangParser.K_THROW, 0)

        def expr(self):
            return self.getTypedRuleContext(DuanLangParser.ExprContext,0)


        def DOT(self):
            return self.getToken(DuanLangParser.DOT, 0)

        def getRuleIndex(self):
            return DuanLangParser.RULE_throwStmt

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitThrowStmt" ):
                return visitor.visitThrowStmt(self)
            else:
                return visitor.visitChildren(self)




    def throwStmt(self):

        localctx = DuanLangParser.ThrowStmtContext(self, self._ctx, self.state)
        self.enterRule(localctx, 54, self.RULE_throwStmt)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 356
            self.match(DuanLangParser.K_THROW)
            self.state = 357
            self.expr()
            self.state = 359
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==82:
                self.state = 358
                self.match(DuanLangParser.DOT)


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class PrintStmtContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def expr(self):
            return self.getTypedRuleContext(DuanLangParser.ExprContext,0)


        def K_PRINT(self):
            return self.getToken(DuanLangParser.K_PRINT, 0)

        def K_OUTPUT(self):
            return self.getToken(DuanLangParser.K_OUTPUT, 0)

        def DOT(self):
            return self.getToken(DuanLangParser.DOT, 0)

        def getRuleIndex(self):
            return DuanLangParser.RULE_printStmt

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitPrintStmt" ):
                return visitor.visitPrintStmt(self)
            else:
                return visitor.visitChildren(self)




    def printStmt(self):

        localctx = DuanLangParser.PrintStmtContext(self, self._ctx, self.state)
        self.enterRule(localctx, 56, self.RULE_printStmt)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 361
            _la = self._input.LA(1)
            if not(_la==33 or _la==34):
                self._errHandler.recoverInline(self)
            else:
                self._errHandler.reportMatch(self)
                self.consume()
            self.state = 362
            self.expr()
            self.state = 364
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==82:
                self.state = 363
                self.match(DuanLangParser.DOT)


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ExprStmtContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def expr(self):
            return self.getTypedRuleContext(DuanLangParser.ExprContext,0)


        def DOT(self):
            return self.getToken(DuanLangParser.DOT, 0)

        def getRuleIndex(self):
            return DuanLangParser.RULE_exprStmt

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitExprStmt" ):
                return visitor.visitExprStmt(self)
            else:
                return visitor.visitChildren(self)




    def exprStmt(self):

        localctx = DuanLangParser.ExprStmtContext(self, self._ctx, self.state)
        self.enterRule(localctx, 58, self.RULE_exprStmt)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 366
            self.expr()
            self.state = 368
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==82:
                self.state = 367
                self.match(DuanLangParser.DOT)


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ExprContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def pipelineExpr(self):
            return self.getTypedRuleContext(DuanLangParser.PipelineExprContext,0)


        def getRuleIndex(self):
            return DuanLangParser.RULE_expr

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitExpr" ):
                return visitor.visitExpr(self)
            else:
                return visitor.visitChildren(self)




    def expr(self):

        localctx = DuanLangParser.ExprContext(self, self._ctx, self.state)
        self.enterRule(localctx, 60, self.RULE_expr)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 370
            self.pipelineExpr()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class PipelineExprContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def andExpr(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(DuanLangParser.AndExprContext)
            else:
                return self.getTypedRuleContext(DuanLangParser.AndExprContext,i)


        def PIPE(self, i:int=None):
            if i is None:
                return self.getTokens(DuanLangParser.PIPE)
            else:
                return self.getToken(DuanLangParser.PIPE, i)

        def K_AND_WORD(self, i:int=None):
            if i is None:
                return self.getTokens(DuanLangParser.K_AND_WORD)
            else:
                return self.getToken(DuanLangParser.K_AND_WORD, i)

        def getRuleIndex(self):
            return DuanLangParser.RULE_pipelineExpr

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitPipelineExpr" ):
                return visitor.visitPipelineExpr(self)
            else:
                return visitor.visitChildren(self)




    def pipelineExpr(self):

        localctx = DuanLangParser.PipelineExprContext(self, self._ctx, self.state)
        self.enterRule(localctx, 62, self.RULE_pipelineExpr)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 372
            self.andExpr()
            self.state = 377
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==50 or _la==80:
                self.state = 373
                _la = self._input.LA(1)
                if not(_la==50 or _la==80):
                    self._errHandler.recoverInline(self)
                else:
                    self._errHandler.reportMatch(self)
                    self.consume()
                self.state = 374
                self.andExpr()
                self.state = 379
                self._errHandler.sync(self)
                _la = self._input.LA(1)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class AndExprContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def orExpr(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(DuanLangParser.OrExprContext)
            else:
                return self.getTypedRuleContext(DuanLangParser.OrExprContext,i)


        def K_AND(self, i:int=None):
            if i is None:
                return self.getTokens(DuanLangParser.K_AND)
            else:
                return self.getToken(DuanLangParser.K_AND, i)

        def getRuleIndex(self):
            return DuanLangParser.RULE_andExpr

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitAndExpr" ):
                return visitor.visitAndExpr(self)
            else:
                return visitor.visitChildren(self)




    def andExpr(self):

        localctx = DuanLangParser.AndExprContext(self, self._ctx, self.state)
        self.enterRule(localctx, 64, self.RULE_andExpr)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 380
            self.orExpr()
            self.state = 385
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==41:
                self.state = 381
                self.match(DuanLangParser.K_AND)
                self.state = 382
                self.orExpr()
                self.state = 387
                self._errHandler.sync(self)
                _la = self._input.LA(1)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class OrExprContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def comparisonExpr(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(DuanLangParser.ComparisonExprContext)
            else:
                return self.getTypedRuleContext(DuanLangParser.ComparisonExprContext,i)


        def K_OR(self, i:int=None):
            if i is None:
                return self.getTokens(DuanLangParser.K_OR)
            else:
                return self.getToken(DuanLangParser.K_OR, i)

        def getRuleIndex(self):
            return DuanLangParser.RULE_orExpr

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitOrExpr" ):
                return visitor.visitOrExpr(self)
            else:
                return visitor.visitChildren(self)




    def orExpr(self):

        localctx = DuanLangParser.OrExprContext(self, self._ctx, self.state)
        self.enterRule(localctx, 66, self.RULE_orExpr)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 388
            self.comparisonExpr()
            self.state = 393
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==42:
                self.state = 389
                self.match(DuanLangParser.K_OR)
                self.state = 390
                self.comparisonExpr()
                self.state = 395
                self._errHandler.sync(self)
                _la = self._input.LA(1)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ComparisonExprContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def additiveExpr(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(DuanLangParser.AdditiveExprContext)
            else:
                return self.getTypedRuleContext(DuanLangParser.AdditiveExprContext,i)


        def compOp(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(DuanLangParser.CompOpContext)
            else:
                return self.getTypedRuleContext(DuanLangParser.CompOpContext,i)


        def getRuleIndex(self):
            return DuanLangParser.RULE_comparisonExpr

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitComparisonExpr" ):
                return visitor.visitComparisonExpr(self)
            else:
                return visitor.visitChildren(self)




    def comparisonExpr(self):

        localctx = DuanLangParser.ComparisonExprContext(self, self._ctx, self.state)
        self.enterRule(localctx, 68, self.RULE_comparisonExpr)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 396
            self.additiveExpr()
            self.state = 402
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while (((_la) & ~0x3f) == 0 and ((1 << _la) & 97280) != 0) or ((((_la - 71)) & ~0x3f) == 0 and ((1 << (_la - 71)) & 63) != 0):
                self.state = 397
                self.compOp()
                self.state = 398
                self.additiveExpr()
                self.state = 404
                self._errHandler.sync(self)
                _la = self._input.LA(1)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class CompOpContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def K_GE(self):
            return self.getToken(DuanLangParser.K_GE, 0)

        def K_LE(self):
            return self.getToken(DuanLangParser.K_LE, 0)

        def K_GT(self):
            return self.getToken(DuanLangParser.K_GT, 0)

        def K_LT(self):
            return self.getToken(DuanLangParser.K_LT, 0)

        def K_NE(self):
            return self.getToken(DuanLangParser.K_NE, 0)

        def K_EQUAL(self):
            return self.getToken(DuanLangParser.K_EQUAL, 0)

        def GE(self):
            return self.getToken(DuanLangParser.GE, 0)

        def LE(self):
            return self.getToken(DuanLangParser.LE, 0)

        def GT(self):
            return self.getToken(DuanLangParser.GT, 0)

        def LT(self):
            return self.getToken(DuanLangParser.LT, 0)

        def NE(self):
            return self.getToken(DuanLangParser.NE, 0)

        def EQ(self):
            return self.getToken(DuanLangParser.EQ, 0)

        def getRuleIndex(self):
            return DuanLangParser.RULE_compOp

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitCompOp" ):
                return visitor.visitCompOp(self)
            else:
                return visitor.visitChildren(self)




    def compOp(self):

        localctx = DuanLangParser.CompOpContext(self, self._ctx, self.state)
        self.enterRule(localctx, 70, self.RULE_compOp)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 405
            _la = self._input.LA(1)
            if not((((_la) & ~0x3f) == 0 and ((1 << _la) & 97280) != 0) or ((((_la - 71)) & ~0x3f) == 0 and ((1 << (_la - 71)) & 63) != 0)):
                self._errHandler.recoverInline(self)
            else:
                self._errHandler.reportMatch(self)
                self.consume()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class AdditiveExprContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def multiplicativeExpr(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(DuanLangParser.MultiplicativeExprContext)
            else:
                return self.getTypedRuleContext(DuanLangParser.MultiplicativeExprContext,i)


        def addOp(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(DuanLangParser.AddOpContext)
            else:
                return self.getTypedRuleContext(DuanLangParser.AddOpContext,i)


        def getRuleIndex(self):
            return DuanLangParser.RULE_additiveExpr

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitAdditiveExpr" ):
                return visitor.visitAdditiveExpr(self)
            else:
                return visitor.visitChildren(self)




    def additiveExpr(self):

        localctx = DuanLangParser.AdditiveExprContext(self, self._ctx, self.state)
        self.enterRule(localctx, 72, self.RULE_additiveExpr)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 407
            self.multiplicativeExpr()
            self.state = 413
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,49,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    self.state = 408
                    self.addOp()
                    self.state = 409
                    self.multiplicativeExpr() 
                self.state = 415
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,49,self._ctx)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class AddOpContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def K_PLUS(self):
            return self.getToken(DuanLangParser.K_PLUS, 0)

        def K_MINUS(self):
            return self.getToken(DuanLangParser.K_MINUS, 0)

        def PLUS(self):
            return self.getToken(DuanLangParser.PLUS, 0)

        def MINUS(self):
            return self.getToken(DuanLangParser.MINUS, 0)

        def getRuleIndex(self):
            return DuanLangParser.RULE_addOp

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitAddOp" ):
                return visitor.visitAddOp(self)
            else:
                return visitor.visitChildren(self)




    def addOp(self):

        localctx = DuanLangParser.AddOpContext(self, self._ctx, self.state)
        self.enterRule(localctx, 74, self.RULE_addOp)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 416
            _la = self._input.LA(1)
            if not(((((_la - 44)) & ~0x3f) == 0 and ((1 << (_la - 44)) & 100663299) != 0)):
                self._errHandler.recoverInline(self)
            else:
                self._errHandler.reportMatch(self)
                self.consume()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class MultiplicativeExprContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def unaryExpr(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(DuanLangParser.UnaryExprContext)
            else:
                return self.getTypedRuleContext(DuanLangParser.UnaryExprContext,i)


        def multOp(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(DuanLangParser.MultOpContext)
            else:
                return self.getTypedRuleContext(DuanLangParser.MultOpContext,i)


        def getRuleIndex(self):
            return DuanLangParser.RULE_multiplicativeExpr

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitMultiplicativeExpr" ):
                return visitor.visitMultiplicativeExpr(self)
            else:
                return visitor.visitChildren(self)




    def multiplicativeExpr(self):

        localctx = DuanLangParser.MultiplicativeExprContext(self, self._ctx, self.state)
        self.enterRule(localctx, 76, self.RULE_multiplicativeExpr)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 418
            self.unaryExpr()
            self.state = 424
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while ((((_la - 46)) & ~0x3f) == 0 and ((1 << (_la - 46)) & 7864335) != 0):
                self.state = 419
                self.multOp()
                self.state = 420
                self.unaryExpr()
                self.state = 426
                self._errHandler.sync(self)
                _la = self._input.LA(1)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class MultOpContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def K_MULTIPLY(self):
            return self.getToken(DuanLangParser.K_MULTIPLY, 0)

        def K_DIVIDE(self):
            return self.getToken(DuanLangParser.K_DIVIDE, 0)

        def K_MOD(self):
            return self.getToken(DuanLangParser.K_MOD, 0)

        def K_POW(self):
            return self.getToken(DuanLangParser.K_POW, 0)

        def MULTIPLY(self):
            return self.getToken(DuanLangParser.MULTIPLY, 0)

        def DIVIDE(self):
            return self.getToken(DuanLangParser.DIVIDE, 0)

        def MODULO(self):
            return self.getToken(DuanLangParser.MODULO, 0)

        def POW(self):
            return self.getToken(DuanLangParser.POW, 0)

        def getRuleIndex(self):
            return DuanLangParser.RULE_multOp

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitMultOp" ):
                return visitor.visitMultOp(self)
            else:
                return visitor.visitChildren(self)




    def multOp(self):

        localctx = DuanLangParser.MultOpContext(self, self._ctx, self.state)
        self.enterRule(localctx, 78, self.RULE_multOp)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 427
            _la = self._input.LA(1)
            if not(((((_la - 46)) & ~0x3f) == 0 and ((1 << (_la - 46)) & 7864335) != 0)):
                self._errHandler.recoverInline(self)
            else:
                self._errHandler.reportMatch(self)
                self.consume()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class UnaryExprContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def unaryExpr(self):
            return self.getTypedRuleContext(DuanLangParser.UnaryExprContext,0)


        def K_NOT(self):
            return self.getToken(DuanLangParser.K_NOT, 0)

        def NOT(self):
            return self.getToken(DuanLangParser.NOT, 0)

        def MINUS(self):
            return self.getToken(DuanLangParser.MINUS, 0)

        def K_MINUS(self):
            return self.getToken(DuanLangParser.K_MINUS, 0)

        def postfixExpr(self):
            return self.getTypedRuleContext(DuanLangParser.PostfixExprContext,0)


        def getRuleIndex(self):
            return DuanLangParser.RULE_unaryExpr

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitUnaryExpr" ):
                return visitor.visitUnaryExpr(self)
            else:
                return visitor.visitChildren(self)




    def unaryExpr(self):

        localctx = DuanLangParser.UnaryExprContext(self, self._ctx, self.state)
        self.enterRule(localctx, 80, self.RULE_unaryExpr)
        self._la = 0 # Token type
        try:
            self.state = 434
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [43, 77]:
                self.enterOuterAlt(localctx, 1)
                self.state = 429
                _la = self._input.LA(1)
                if not(_la==43 or _la==77):
                    self._errHandler.recoverInline(self)
                else:
                    self._errHandler.reportMatch(self)
                    self.consume()
                self.state = 430
                self.unaryExpr()
                pass
            elif token in [45, 70]:
                self.enterOuterAlt(localctx, 2)
                self.state = 431
                _la = self._input.LA(1)
                if not(_la==45 or _la==70):
                    self._errHandler.recoverInline(self)
                else:
                    self._errHandler.reportMatch(self)
                    self.consume()
                self.state = 432
                self.unaryExpr()
                pass
            elif token in [53, 54, 55, 87, 89, 93, 95, 96, 97]:
                self.enterOuterAlt(localctx, 3)
                self.state = 433
                self.postfixExpr()
                pass
            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class PostfixExprContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def primary(self):
            return self.getTypedRuleContext(DuanLangParser.PrimaryContext,0)


        def BOOK_L(self, i:int=None):
            if i is None:
                return self.getTokens(DuanLangParser.BOOK_L)
            else:
                return self.getToken(DuanLangParser.BOOK_L, i)

        def ID(self, i:int=None):
            if i is None:
                return self.getTokens(DuanLangParser.ID)
            else:
                return self.getToken(DuanLangParser.ID, i)

        def BOOK_R(self, i:int=None):
            if i is None:
                return self.getTokens(DuanLangParser.BOOK_R)
            else:
                return self.getToken(DuanLangParser.BOOK_R, i)

        def LPAREN(self, i:int=None):
            if i is None:
                return self.getTokens(DuanLangParser.LPAREN)
            else:
                return self.getToken(DuanLangParser.LPAREN, i)

        def RPAREN(self, i:int=None):
            if i is None:
                return self.getTokens(DuanLangParser.RPAREN)
            else:
                return self.getToken(DuanLangParser.RPAREN, i)

        def K_OF(self, i:int=None):
            if i is None:
                return self.getTokens(DuanLangParser.K_OF)
            else:
                return self.getToken(DuanLangParser.K_OF, i)

        def LBRACKET(self, i:int=None):
            if i is None:
                return self.getTokens(DuanLangParser.LBRACKET)
            else:
                return self.getToken(DuanLangParser.LBRACKET, i)

        def expr(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(DuanLangParser.ExprContext)
            else:
                return self.getTypedRuleContext(DuanLangParser.ExprContext,i)


        def RBRACKET(self, i:int=None):
            if i is None:
                return self.getTokens(DuanLangParser.RBRACKET)
            else:
                return self.getToken(DuanLangParser.RBRACKET, i)

        def exprList(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(DuanLangParser.ExprListContext)
            else:
                return self.getTypedRuleContext(DuanLangParser.ExprListContext,i)


        def getRuleIndex(self):
            return DuanLangParser.RULE_postfixExpr

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitPostfixExpr" ):
                return visitor.visitPostfixExpr(self)
            else:
                return visitor.visitChildren(self)




    def postfixExpr(self):

        localctx = DuanLangParser.PostfixExprContext(self, self._ctx, self.state)
        self.enterRule(localctx, 82, self.RULE_postfixExpr)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 436
            self.primary()
            self.state = 458
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,55,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    self.state = 456
                    self._errHandler.sync(self)
                    token = self._input.LA(1)
                    if token in [93]:
                        self.state = 437
                        self.match(DuanLangParser.BOOK_L)
                        self.state = 438
                        self.match(DuanLangParser.ID)
                        self.state = 439
                        self.match(DuanLangParser.BOOK_R)
                        self.state = 440
                        self.match(DuanLangParser.LPAREN)
                        self.state = 442
                        self._errHandler.sync(self)
                        _la = self._input.LA(1)
                        if ((((_la - 43)) & ~0x3f) == 0 and ((1 << (_la - 43)) & 32739075542752261) != 0):
                            self.state = 441
                            self.exprList()


                        self.state = 444
                        self.match(DuanLangParser.RPAREN)
                        pass
                    elif token in [87]:
                        self.state = 445
                        self.match(DuanLangParser.LPAREN)
                        self.state = 447
                        self._errHandler.sync(self)
                        _la = self._input.LA(1)
                        if ((((_la - 43)) & ~0x3f) == 0 and ((1 << (_la - 43)) & 32739075542752261) != 0):
                            self.state = 446
                            self.exprList()


                        self.state = 449
                        self.match(DuanLangParser.RPAREN)
                        pass
                    elif token in [51]:
                        self.state = 450
                        self.match(DuanLangParser.K_OF)
                        self.state = 451
                        self.match(DuanLangParser.ID)
                        pass
                    elif token in [89]:
                        self.state = 452
                        self.match(DuanLangParser.LBRACKET)
                        self.state = 453
                        self.expr()
                        self.state = 454
                        self.match(DuanLangParser.RBRACKET)
                        pass
                    else:
                        raise NoViableAltException(self)
             
                self.state = 460
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,55,self._ctx)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class PrimaryContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def NUMBER(self):
            return self.getToken(DuanLangParser.NUMBER, 0)

        def STRING(self):
            return self.getToken(DuanLangParser.STRING, 0)

        def K_TRUE(self):
            return self.getToken(DuanLangParser.K_TRUE, 0)

        def K_FALSE(self):
            return self.getToken(DuanLangParser.K_FALSE, 0)

        def K_NULL(self):
            return self.getToken(DuanLangParser.K_NULL, 0)

        def ID(self):
            return self.getToken(DuanLangParser.ID, 0)

        def LPAREN(self):
            return self.getToken(DuanLangParser.LPAREN, 0)

        def expr(self):
            return self.getTypedRuleContext(DuanLangParser.ExprContext,0)


        def RPAREN(self):
            return self.getToken(DuanLangParser.RPAREN, 0)

        def LBRACKET(self):
            return self.getToken(DuanLangParser.LBRACKET, 0)

        def RBRACKET(self):
            return self.getToken(DuanLangParser.RBRACKET, 0)

        def exprList(self):
            return self.getTypedRuleContext(DuanLangParser.ExprListContext,0)


        def BOOK_L(self):
            return self.getToken(DuanLangParser.BOOK_L, 0)

        def BOOK_R(self):
            return self.getToken(DuanLangParser.BOOK_R, 0)

        def getRuleIndex(self):
            return DuanLangParser.RULE_primary

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitPrimary" ):
                return visitor.visitPrimary(self)
            else:
                return visitor.visitChildren(self)




    def primary(self):

        localctx = DuanLangParser.PrimaryContext(self, self._ctx, self.state)
        self.enterRule(localctx, 84, self.RULE_primary)
        self._la = 0 # Token type
        try:
            self.state = 479
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [95]:
                self.enterOuterAlt(localctx, 1)
                self.state = 461
                self.match(DuanLangParser.NUMBER)
                pass
            elif token in [96]:
                self.enterOuterAlt(localctx, 2)
                self.state = 462
                self.match(DuanLangParser.STRING)
                pass
            elif token in [53]:
                self.enterOuterAlt(localctx, 3)
                self.state = 463
                self.match(DuanLangParser.K_TRUE)
                pass
            elif token in [54]:
                self.enterOuterAlt(localctx, 4)
                self.state = 464
                self.match(DuanLangParser.K_FALSE)
                pass
            elif token in [55]:
                self.enterOuterAlt(localctx, 5)
                self.state = 465
                self.match(DuanLangParser.K_NULL)
                pass
            elif token in [97]:
                self.enterOuterAlt(localctx, 6)
                self.state = 466
                self.match(DuanLangParser.ID)
                pass
            elif token in [87]:
                self.enterOuterAlt(localctx, 7)
                self.state = 467
                self.match(DuanLangParser.LPAREN)
                self.state = 468
                self.expr()
                self.state = 469
                self.match(DuanLangParser.RPAREN)
                pass
            elif token in [89]:
                self.enterOuterAlt(localctx, 8)
                self.state = 471
                self.match(DuanLangParser.LBRACKET)
                self.state = 473
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if ((((_la - 43)) & ~0x3f) == 0 and ((1 << (_la - 43)) & 32739075542752261) != 0):
                    self.state = 472
                    self.exprList()


                self.state = 475
                self.match(DuanLangParser.RBRACKET)
                pass
            elif token in [93]:
                self.enterOuterAlt(localctx, 9)
                self.state = 476
                self.match(DuanLangParser.BOOK_L)
                self.state = 477
                self.match(DuanLangParser.ID)
                self.state = 478
                self.match(DuanLangParser.BOOK_R)
                pass
            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class TypeAnnotationContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def builtinType(self):
            return self.getTypedRuleContext(DuanLangParser.BuiltinTypeContext,0)


        def ID(self):
            return self.getToken(DuanLangParser.ID, 0)

        def getRuleIndex(self):
            return DuanLangParser.RULE_typeAnnotation

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitTypeAnnotation" ):
                return visitor.visitTypeAnnotation(self)
            else:
                return visitor.visitChildren(self)




    def typeAnnotation(self):

        localctx = DuanLangParser.TypeAnnotationContext(self, self._ctx, self.state)
        self.enterRule(localctx, 86, self.RULE_typeAnnotation)
        try:
            self.state = 483
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [55, 56, 57, 58, 59, 60, 61, 62, 63, 64]:
                self.enterOuterAlt(localctx, 1)
                self.state = 481
                self.builtinType()
                pass
            elif token in [97]:
                self.enterOuterAlt(localctx, 2)
                self.state = 482
                self.match(DuanLangParser.ID)
                pass
            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class BuiltinTypeContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def T_NUMBER(self):
            return self.getToken(DuanLangParser.T_NUMBER, 0)

        def T_INT(self):
            return self.getToken(DuanLangParser.T_INT, 0)

        def T_FLOAT(self):
            return self.getToken(DuanLangParser.T_FLOAT, 0)

        def T_STRING(self):
            return self.getToken(DuanLangParser.T_STRING, 0)

        def T_LIST(self):
            return self.getToken(DuanLangParser.T_LIST, 0)

        def T_DICT(self):
            return self.getToken(DuanLangParser.T_DICT, 0)

        def T_SET(self):
            return self.getToken(DuanLangParser.T_SET, 0)

        def T_BOOL(self):
            return self.getToken(DuanLangParser.T_BOOL, 0)

        def K_NULL(self):
            return self.getToken(DuanLangParser.K_NULL, 0)

        def T_ANY(self):
            return self.getToken(DuanLangParser.T_ANY, 0)

        def getRuleIndex(self):
            return DuanLangParser.RULE_builtinType

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitBuiltinType" ):
                return visitor.visitBuiltinType(self)
            else:
                return visitor.visitChildren(self)




    def builtinType(self):

        localctx = DuanLangParser.BuiltinTypeContext(self, self._ctx, self.state)
        self.enterRule(localctx, 88, self.RULE_builtinType)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 485
            _la = self._input.LA(1)
            if not(((((_la - 55)) & ~0x3f) == 0 and ((1 << (_la - 55)) & 1023) != 0)):
                self._errHandler.recoverInline(self)
            else:
                self._errHandler.reportMatch(self)
                self.consume()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ExprListContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def expr(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(DuanLangParser.ExprContext)
            else:
                return self.getTypedRuleContext(DuanLangParser.ExprContext,i)


        def COMMA(self, i:int=None):
            if i is None:
                return self.getTokens(DuanLangParser.COMMA)
            else:
                return self.getToken(DuanLangParser.COMMA, i)

        def getRuleIndex(self):
            return DuanLangParser.RULE_exprList

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitExprList" ):
                return visitor.visitExprList(self)
            else:
                return visitor.visitChildren(self)




    def exprList(self):

        localctx = DuanLangParser.ExprListContext(self, self._ctx, self.state)
        self.enterRule(localctx, 90, self.RULE_exprList)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 487
            self.expr()
            self.state = 492
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==83:
                self.state = 488
                self.match(DuanLangParser.COMMA)
                self.state = 489
                self.expr()
                self.state = 494
                self._errHandler.sync(self)
                _la = self._input.LA(1)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx





