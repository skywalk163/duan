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
        4,1,112,692,2,0,7,0,2,1,7,1,2,2,7,2,2,3,7,3,2,4,7,4,2,5,7,5,2,6,
        7,6,2,7,7,7,2,8,7,8,2,9,7,9,2,10,7,10,2,11,7,11,2,12,7,12,2,13,7,
        13,2,14,7,14,2,15,7,15,2,16,7,16,2,17,7,17,2,18,7,18,2,19,7,19,2,
        20,7,20,2,21,7,21,2,22,7,22,2,23,7,23,2,24,7,24,2,25,7,25,2,26,7,
        26,2,27,7,27,2,28,7,28,2,29,7,29,2,30,7,30,2,31,7,31,2,32,7,32,2,
        33,7,33,2,34,7,34,2,35,7,35,2,36,7,36,2,37,7,37,2,38,7,38,2,39,7,
        39,2,40,7,40,2,41,7,41,2,42,7,42,2,43,7,43,2,44,7,44,2,45,7,45,2,
        46,7,46,2,47,7,47,2,48,7,48,2,49,7,49,2,50,7,50,2,51,7,51,2,52,7,
        52,2,53,7,53,2,54,7,54,2,55,7,55,1,0,1,0,1,0,1,0,1,0,5,0,118,8,0,
        10,0,12,0,121,9,0,1,0,1,0,1,1,1,1,1,1,1,1,1,2,1,2,1,2,1,2,1,2,3,
        2,134,8,2,1,3,1,3,1,3,1,3,3,3,140,8,3,1,3,1,3,3,3,144,8,3,1,3,1,
        3,1,3,1,3,3,3,150,8,3,1,4,1,4,1,4,3,4,155,8,4,1,4,1,4,1,4,1,4,5,
        4,161,8,4,10,4,12,4,164,9,4,3,4,166,8,4,1,4,1,4,1,4,1,4,5,4,172,
        8,4,10,4,12,4,175,9,4,3,4,177,8,4,1,4,1,4,5,4,181,8,4,10,4,12,4,
        184,9,4,1,4,1,4,3,4,188,8,4,1,5,1,5,1,5,1,5,5,5,194,8,5,10,5,12,
        5,197,9,5,1,5,1,5,1,6,1,6,1,6,1,6,3,6,205,8,6,1,7,1,7,1,7,1,7,3,
        7,211,8,7,1,7,1,7,3,7,215,8,7,1,7,1,7,1,7,1,7,3,7,221,8,7,1,8,1,
        8,1,8,3,8,226,8,8,1,8,1,8,1,8,3,8,231,8,8,1,8,1,8,1,8,1,8,3,8,237,
        8,8,1,9,1,9,1,9,1,9,3,9,243,8,9,1,9,1,9,3,9,247,8,9,1,9,3,9,250,
        8,9,1,10,1,10,1,10,1,10,1,10,1,10,5,10,258,8,10,10,10,12,10,261,
        9,10,3,10,263,8,10,1,10,1,10,5,10,267,8,10,10,10,12,10,270,9,10,
        1,10,1,10,3,10,274,8,10,1,11,1,11,1,11,1,11,3,11,280,8,11,1,11,1,
        11,1,11,3,11,285,8,11,1,11,3,11,288,8,11,1,12,1,12,1,12,5,12,293,
        8,12,10,12,12,12,296,9,12,1,13,1,13,1,13,3,13,301,8,13,1,13,1,13,
        3,13,305,8,13,1,14,5,14,308,8,14,10,14,12,14,311,9,14,1,15,1,15,
        1,15,1,15,1,15,1,15,4,15,319,8,15,11,15,12,15,320,1,15,1,15,3,15,
        325,8,15,1,16,1,16,1,16,1,16,3,16,331,8,16,1,17,1,17,1,17,1,17,1,
        17,1,17,4,17,339,8,17,11,17,12,17,340,1,17,1,17,3,17,345,8,17,1,
        18,1,18,1,18,1,18,1,18,3,18,352,8,18,1,18,1,18,1,18,3,18,357,8,18,
        3,18,359,8,18,1,19,1,19,1,19,1,19,1,19,3,19,366,8,19,1,19,3,19,369,
        8,19,1,20,1,20,1,20,5,20,374,8,20,10,20,12,20,377,9,20,1,20,1,20,
        1,20,3,20,382,8,20,1,21,1,21,1,21,5,21,387,8,21,10,21,12,21,390,
        9,21,1,22,1,22,1,22,1,22,3,22,396,8,22,1,23,1,23,1,23,1,23,1,23,
        1,23,1,23,1,23,1,23,1,23,1,23,1,23,3,23,410,8,23,1,24,1,24,1,24,
        1,24,1,24,1,24,1,24,3,24,419,8,24,1,24,1,24,1,24,1,24,1,24,1,24,
        3,24,427,8,24,3,24,429,8,24,1,25,1,25,1,25,1,25,3,25,435,8,25,1,
        26,1,26,1,26,1,26,1,26,1,26,1,26,1,26,1,26,3,26,446,8,26,1,27,1,
        27,1,27,1,27,1,27,1,27,1,27,1,27,1,27,5,27,457,8,27,10,27,12,27,
        460,9,27,1,27,1,27,1,27,3,27,465,8,27,1,27,1,27,3,27,469,8,27,1,
        28,1,28,1,28,1,28,1,28,1,28,1,28,1,28,3,28,479,8,28,1,29,1,29,1,
        29,1,29,1,29,1,29,1,29,1,29,1,29,3,29,490,8,29,1,30,1,30,1,30,1,
        30,3,30,496,8,30,1,30,1,30,3,30,500,8,30,1,31,1,31,3,31,504,8,31,
        1,31,3,31,507,8,31,1,32,1,32,3,32,511,8,32,1,33,1,33,3,33,515,8,
        33,1,34,1,34,1,34,1,34,1,34,1,34,1,34,1,34,1,34,3,34,526,8,34,1,
        35,1,35,1,35,3,35,531,8,35,1,36,1,36,1,36,3,36,536,8,36,1,37,1,37,
        1,37,1,38,1,38,1,39,1,39,1,39,5,39,546,8,39,10,39,12,39,549,9,39,
        1,40,1,40,1,40,5,40,554,8,40,10,40,12,40,557,9,40,1,41,1,41,1,41,
        5,41,562,8,41,10,41,12,41,565,9,41,1,42,1,42,1,42,1,42,5,42,571,
        8,42,10,42,12,42,574,9,42,1,43,1,43,1,44,1,44,1,44,1,44,5,44,582,
        8,44,10,44,12,44,585,9,44,1,45,1,45,1,46,1,46,1,46,1,46,5,46,593,
        8,46,10,46,12,46,596,9,46,1,47,1,47,1,48,1,48,1,48,1,48,1,48,3,48,
        605,8,48,1,49,1,49,1,49,1,49,1,49,1,49,3,49,613,8,49,1,49,1,49,1,
        49,3,49,618,8,49,1,49,1,49,1,49,1,49,1,49,1,49,1,49,1,49,1,49,5,
        49,629,8,49,10,49,12,49,632,9,49,1,50,1,50,1,50,1,50,1,50,1,50,1,
        50,1,50,1,50,1,50,3,50,644,8,50,1,50,1,50,1,50,1,50,1,50,1,50,1,
        50,1,50,1,50,1,50,1,50,1,50,3,50,658,8,50,1,50,1,50,1,50,1,50,3,
        50,664,8,50,1,51,1,51,1,51,5,51,669,8,51,10,51,12,51,672,9,51,1,
        52,1,52,1,52,1,52,1,53,1,53,3,53,680,8,53,1,54,1,54,1,55,1,55,1,
        55,5,55,687,8,55,10,55,12,55,690,9,55,1,55,0,0,56,0,2,4,6,8,10,12,
        14,16,18,20,22,24,26,28,30,32,34,36,38,40,42,44,46,48,50,52,54,56,
        58,60,62,64,66,68,70,72,74,76,78,80,82,84,86,88,90,92,94,96,98,100,
        102,104,106,108,110,0,10,3,0,16,16,18,18,87,87,1,0,60,61,1,0,36,
        37,2,0,59,59,91,91,3,0,10,14,18,18,81,86,2,0,53,54,79,80,2,0,55,
        58,75,78,2,0,52,52,88,88,2,0,54,54,80,80,1,0,65,74,756,0,119,1,0,
        0,0,2,124,1,0,0,0,4,133,1,0,0,0,6,135,1,0,0,0,8,151,1,0,0,0,10,189,
        1,0,0,0,12,204,1,0,0,0,14,206,1,0,0,0,16,222,1,0,0,0,18,238,1,0,
        0,0,20,251,1,0,0,0,22,275,1,0,0,0,24,289,1,0,0,0,26,297,1,0,0,0,
        28,309,1,0,0,0,30,312,1,0,0,0,32,326,1,0,0,0,34,332,1,0,0,0,36,358,
        1,0,0,0,38,360,1,0,0,0,40,381,1,0,0,0,42,383,1,0,0,0,44,395,1,0,
        0,0,46,409,1,0,0,0,48,428,1,0,0,0,50,430,1,0,0,0,52,445,1,0,0,0,
        54,447,1,0,0,0,56,470,1,0,0,0,58,489,1,0,0,0,60,491,1,0,0,0,62,501,
        1,0,0,0,64,508,1,0,0,0,66,512,1,0,0,0,68,516,1,0,0,0,70,527,1,0,
        0,0,72,532,1,0,0,0,74,537,1,0,0,0,76,540,1,0,0,0,78,542,1,0,0,0,
        80,550,1,0,0,0,82,558,1,0,0,0,84,566,1,0,0,0,86,575,1,0,0,0,88,577,
        1,0,0,0,90,586,1,0,0,0,92,588,1,0,0,0,94,597,1,0,0,0,96,604,1,0,
        0,0,98,606,1,0,0,0,100,663,1,0,0,0,102,665,1,0,0,0,104,673,1,0,0,
        0,106,679,1,0,0,0,108,681,1,0,0,0,110,683,1,0,0,0,112,118,3,2,1,
        0,113,118,3,36,18,0,114,118,3,38,19,0,115,118,3,4,2,0,116,118,3,
        46,23,0,117,112,1,0,0,0,117,113,1,0,0,0,117,114,1,0,0,0,117,115,
        1,0,0,0,117,116,1,0,0,0,118,121,1,0,0,0,119,117,1,0,0,0,119,120,
        1,0,0,0,120,122,1,0,0,0,121,119,1,0,0,0,122,123,5,0,0,1,123,1,1,
        0,0,0,124,125,5,101,0,0,125,126,5,109,0,0,126,127,5,102,0,0,127,
        3,1,0,0,0,128,134,3,6,3,0,129,134,3,8,4,0,130,134,3,20,10,0,131,
        134,3,30,15,0,132,134,3,34,17,0,133,128,1,0,0,0,133,129,1,0,0,0,
        133,130,1,0,0,0,133,131,1,0,0,0,133,132,1,0,0,0,134,5,1,0,0,0,135,
        136,5,19,0,0,136,139,5,109,0,0,137,138,5,20,0,0,138,140,3,24,12,
        0,139,137,1,0,0,0,139,140,1,0,0,0,140,143,1,0,0,0,141,142,5,35,0,
        0,142,144,3,106,53,0,143,141,1,0,0,0,143,144,1,0,0,0,144,145,1,0,
        0,0,145,146,5,96,0,0,146,147,3,28,14,0,147,149,5,9,0,0,148,150,5,
        94,0,0,149,148,1,0,0,0,149,150,1,0,0,0,150,7,1,0,0,0,151,152,5,39,
        0,0,152,154,5,109,0,0,153,155,3,10,5,0,154,153,1,0,0,0,154,155,1,
        0,0,0,155,165,1,0,0,0,156,157,5,41,0,0,157,162,3,106,53,0,158,159,
        5,95,0,0,159,161,3,106,53,0,160,158,1,0,0,0,161,164,1,0,0,0,162,
        160,1,0,0,0,162,163,1,0,0,0,163,166,1,0,0,0,164,162,1,0,0,0,165,
        156,1,0,0,0,165,166,1,0,0,0,166,176,1,0,0,0,167,168,5,42,0,0,168,
        173,3,106,53,0,169,170,5,95,0,0,170,172,3,106,53,0,171,169,1,0,0,
        0,172,175,1,0,0,0,173,171,1,0,0,0,173,174,1,0,0,0,174,177,1,0,0,
        0,175,173,1,0,0,0,176,167,1,0,0,0,176,177,1,0,0,0,177,178,1,0,0,
        0,178,182,5,96,0,0,179,181,3,12,6,0,180,179,1,0,0,0,181,184,1,0,
        0,0,182,180,1,0,0,0,182,183,1,0,0,0,183,185,1,0,0,0,184,182,1,0,
        0,0,185,187,5,9,0,0,186,188,5,94,0,0,187,186,1,0,0,0,187,188,1,0,
        0,0,188,9,1,0,0,0,189,190,5,101,0,0,190,195,5,109,0,0,191,192,5,
        95,0,0,192,194,5,109,0,0,193,191,1,0,0,0,194,197,1,0,0,0,195,193,
        1,0,0,0,195,196,1,0,0,0,196,198,1,0,0,0,197,195,1,0,0,0,198,199,
        5,102,0,0,199,11,1,0,0,0,200,205,3,14,7,0,201,205,3,16,8,0,202,205,
        3,18,9,0,203,205,3,46,23,0,204,200,1,0,0,0,204,201,1,0,0,0,204,202,
        1,0,0,0,204,203,1,0,0,0,205,13,1,0,0,0,206,207,5,19,0,0,207,210,
        5,109,0,0,208,209,5,20,0,0,209,211,3,24,12,0,210,208,1,0,0,0,210,
        211,1,0,0,0,211,214,1,0,0,0,212,213,5,35,0,0,213,215,3,106,53,0,
        214,212,1,0,0,0,214,215,1,0,0,0,215,216,1,0,0,0,216,217,5,96,0,0,
        217,218,3,28,14,0,218,220,5,9,0,0,219,221,5,94,0,0,220,219,1,0,0,
        0,220,221,1,0,0,0,221,15,1,0,0,0,222,230,5,48,0,0,223,225,5,99,0,
        0,224,226,3,24,12,0,225,224,1,0,0,0,225,226,1,0,0,0,226,227,1,0,
        0,0,227,231,5,100,0,0,228,229,5,20,0,0,229,231,3,24,12,0,230,223,
        1,0,0,0,230,228,1,0,0,0,230,231,1,0,0,0,231,232,1,0,0,0,232,233,
        5,96,0,0,233,234,3,28,14,0,234,236,5,9,0,0,235,237,5,94,0,0,236,
        235,1,0,0,0,236,237,1,0,0,0,237,17,1,0,0,0,238,239,5,47,0,0,239,
        242,5,109,0,0,240,241,5,16,0,0,241,243,3,106,53,0,242,240,1,0,0,
        0,242,243,1,0,0,0,243,246,1,0,0,0,244,245,5,18,0,0,245,247,3,76,
        38,0,246,244,1,0,0,0,246,247,1,0,0,0,247,249,1,0,0,0,248,250,5,94,
        0,0,249,248,1,0,0,0,249,250,1,0,0,0,250,19,1,0,0,0,251,252,5,40,
        0,0,252,262,5,109,0,0,253,254,5,41,0,0,254,259,3,106,53,0,255,256,
        5,95,0,0,256,258,3,106,53,0,257,255,1,0,0,0,258,261,1,0,0,0,259,
        257,1,0,0,0,259,260,1,0,0,0,260,263,1,0,0,0,261,259,1,0,0,0,262,
        253,1,0,0,0,262,263,1,0,0,0,263,264,1,0,0,0,264,268,5,96,0,0,265,
        267,3,22,11,0,266,265,1,0,0,0,267,270,1,0,0,0,268,266,1,0,0,0,268,
        269,1,0,0,0,269,271,1,0,0,0,270,268,1,0,0,0,271,273,5,9,0,0,272,
        274,5,94,0,0,273,272,1,0,0,0,273,274,1,0,0,0,274,21,1,0,0,0,275,
        276,5,46,0,0,276,277,5,109,0,0,277,279,5,99,0,0,278,280,3,24,12,
        0,279,278,1,0,0,0,279,280,1,0,0,0,280,281,1,0,0,0,281,284,5,100,
        0,0,282,283,5,35,0,0,283,285,3,106,53,0,284,282,1,0,0,0,284,285,
        1,0,0,0,285,287,1,0,0,0,286,288,5,94,0,0,287,286,1,0,0,0,287,288,
        1,0,0,0,288,23,1,0,0,0,289,294,3,26,13,0,290,291,5,95,0,0,291,293,
        3,26,13,0,292,290,1,0,0,0,293,296,1,0,0,0,294,292,1,0,0,0,294,295,
        1,0,0,0,295,25,1,0,0,0,296,294,1,0,0,0,297,300,5,109,0,0,298,299,
        5,96,0,0,299,301,3,106,53,0,300,298,1,0,0,0,300,301,1,0,0,0,301,
        304,1,0,0,0,302,303,5,18,0,0,303,305,3,76,38,0,304,302,1,0,0,0,304,
        305,1,0,0,0,305,27,1,0,0,0,306,308,3,46,23,0,307,306,1,0,0,0,308,
        311,1,0,0,0,309,307,1,0,0,0,309,310,1,0,0,0,310,29,1,0,0,0,311,309,
        1,0,0,0,312,313,5,105,0,0,313,314,5,109,0,0,314,315,5,106,0,0,315,
        316,5,21,0,0,316,318,5,96,0,0,317,319,3,32,16,0,318,317,1,0,0,0,
        319,320,1,0,0,0,320,318,1,0,0,0,320,321,1,0,0,0,321,322,1,0,0,0,
        322,324,5,9,0,0,323,325,5,94,0,0,324,323,1,0,0,0,324,325,1,0,0,0,
        325,31,1,0,0,0,326,327,5,109,0,0,327,328,5,96,0,0,328,330,3,106,
        53,0,329,331,5,94,0,0,330,329,1,0,0,0,330,331,1,0,0,0,331,33,1,0,
        0,0,332,333,5,105,0,0,333,334,5,109,0,0,334,335,5,106,0,0,335,336,
        5,22,0,0,336,338,5,96,0,0,337,339,3,32,16,0,338,337,1,0,0,0,339,
        340,1,0,0,0,340,338,1,0,0,0,340,341,1,0,0,0,341,342,1,0,0,0,342,
        344,5,9,0,0,343,345,5,94,0,0,344,343,1,0,0,0,344,345,1,0,0,0,345,
        35,1,0,0,0,346,347,5,27,0,0,347,348,3,40,20,0,348,349,5,26,0,0,349,
        351,3,42,21,0,350,352,5,94,0,0,351,350,1,0,0,0,351,352,1,0,0,0,352,
        359,1,0,0,0,353,354,5,26,0,0,354,356,3,42,21,0,355,357,5,94,0,0,
        356,355,1,0,0,0,356,357,1,0,0,0,357,359,1,0,0,0,358,346,1,0,0,0,
        358,353,1,0,0,0,359,37,1,0,0,0,360,365,5,25,0,0,361,366,5,109,0,
        0,362,363,5,105,0,0,363,364,5,109,0,0,364,366,5,106,0,0,365,361,
        1,0,0,0,365,362,1,0,0,0,366,368,1,0,0,0,367,369,5,94,0,0,368,367,
        1,0,0,0,368,369,1,0,0,0,369,39,1,0,0,0,370,375,5,109,0,0,371,372,
        5,92,0,0,372,374,5,109,0,0,373,371,1,0,0,0,374,377,1,0,0,0,375,373,
        1,0,0,0,375,376,1,0,0,0,376,382,1,0,0,0,377,375,1,0,0,0,378,379,
        5,105,0,0,379,380,5,109,0,0,380,382,5,106,0,0,381,370,1,0,0,0,381,
        378,1,0,0,0,382,41,1,0,0,0,383,388,3,44,22,0,384,385,5,95,0,0,385,
        387,3,44,22,0,386,384,1,0,0,0,387,390,1,0,0,0,388,386,1,0,0,0,388,
        389,1,0,0,0,389,43,1,0,0,0,390,388,1,0,0,0,391,392,5,105,0,0,392,
        393,5,109,0,0,393,396,5,106,0,0,394,396,5,109,0,0,395,391,1,0,0,
        0,395,394,1,0,0,0,396,45,1,0,0,0,397,410,3,48,24,0,398,410,3,50,
        25,0,399,410,3,54,27,0,400,410,3,56,28,0,401,410,3,60,30,0,402,410,
        3,62,31,0,403,410,3,64,32,0,404,410,3,66,33,0,405,410,3,68,34,0,
        406,410,3,70,35,0,407,410,3,72,36,0,408,410,3,74,37,0,409,397,1,
        0,0,0,409,398,1,0,0,0,409,399,1,0,0,0,409,400,1,0,0,0,409,401,1,
        0,0,0,409,402,1,0,0,0,409,403,1,0,0,0,409,404,1,0,0,0,409,405,1,
        0,0,0,409,406,1,0,0,0,409,407,1,0,0,0,409,408,1,0,0,0,410,47,1,0,
        0,0,411,412,5,15,0,0,412,413,5,109,0,0,413,414,5,16,0,0,414,415,
        3,76,38,0,415,418,5,94,0,0,416,417,5,24,0,0,417,419,3,106,53,0,418,
        416,1,0,0,0,418,419,1,0,0,0,419,429,1,0,0,0,420,421,5,17,0,0,421,
        426,5,109,0,0,422,423,5,18,0,0,423,424,3,76,38,0,424,425,5,94,0,
        0,425,427,1,0,0,0,426,422,1,0,0,0,426,427,1,0,0,0,427,429,1,0,0,
        0,428,411,1,0,0,0,428,420,1,0,0,0,429,49,1,0,0,0,430,431,3,52,26,
        0,431,432,7,0,0,0,432,434,3,76,38,0,433,435,5,94,0,0,434,433,1,0,
        0,0,434,435,1,0,0,0,435,51,1,0,0,0,436,446,5,109,0,0,437,438,3,76,
        38,0,438,439,5,60,0,0,439,440,5,109,0,0,440,446,1,0,0,0,441,442,
        3,100,50,0,442,443,5,93,0,0,443,444,5,109,0,0,444,446,1,0,0,0,445,
        436,1,0,0,0,445,437,1,0,0,0,445,441,1,0,0,0,446,53,1,0,0,0,447,448,
        5,6,0,0,448,449,3,76,38,0,449,450,5,96,0,0,450,458,3,28,14,0,451,
        452,5,5,0,0,452,453,3,76,38,0,453,454,5,96,0,0,454,455,3,28,14,0,
        455,457,1,0,0,0,456,451,1,0,0,0,457,460,1,0,0,0,458,456,1,0,0,0,
        458,459,1,0,0,0,459,464,1,0,0,0,460,458,1,0,0,0,461,462,5,8,0,0,
        462,463,5,96,0,0,463,465,3,28,14,0,464,461,1,0,0,0,464,465,1,0,0,
        0,465,466,1,0,0,0,466,468,5,9,0,0,467,469,5,94,0,0,468,467,1,0,0,
        0,468,469,1,0,0,0,469,55,1,0,0,0,470,471,5,28,0,0,471,472,5,109,
        0,0,472,473,7,1,0,0,473,474,3,76,38,0,474,475,5,96,0,0,475,476,3,
        28,14,0,476,478,5,9,0,0,477,479,5,94,0,0,478,477,1,0,0,0,478,479,
        1,0,0,0,479,57,1,0,0,0,480,490,5,109,0,0,481,482,5,109,0,0,482,483,
        5,60,0,0,483,490,5,109,0,0,484,485,5,109,0,0,485,486,5,60,0,0,486,
        487,5,109,0,0,487,488,5,95,0,0,488,490,5,109,0,0,489,480,1,0,0,0,
        489,481,1,0,0,0,489,484,1,0,0,0,490,59,1,0,0,0,491,492,5,29,0,0,
        492,495,3,76,38,0,493,494,5,96,0,0,494,496,3,28,14,0,495,493,1,0,
        0,0,495,496,1,0,0,0,496,497,1,0,0,0,497,499,5,9,0,0,498,500,5,94,
        0,0,499,498,1,0,0,0,499,500,1,0,0,0,500,61,1,0,0,0,501,503,5,35,
        0,0,502,504,3,76,38,0,503,502,1,0,0,0,503,504,1,0,0,0,504,506,1,
        0,0,0,505,507,5,94,0,0,506,505,1,0,0,0,506,507,1,0,0,0,507,63,1,
        0,0,0,508,510,5,30,0,0,509,511,5,94,0,0,510,509,1,0,0,0,510,511,
        1,0,0,0,511,65,1,0,0,0,512,514,5,31,0,0,513,515,5,94,0,0,514,513,
        1,0,0,0,514,515,1,0,0,0,515,67,1,0,0,0,516,517,5,32,0,0,517,518,
        5,96,0,0,518,519,3,28,14,0,519,520,5,33,0,0,520,521,5,109,0,0,521,
        522,5,96,0,0,522,523,3,28,14,0,523,525,5,9,0,0,524,526,5,94,0,0,
        525,524,1,0,0,0,525,526,1,0,0,0,526,69,1,0,0,0,527,528,5,34,0,0,
        528,530,3,76,38,0,529,531,5,94,0,0,530,529,1,0,0,0,530,531,1,0,0,
        0,531,71,1,0,0,0,532,533,7,2,0,0,533,535,3,76,38,0,534,536,5,94,
        0,0,535,534,1,0,0,0,535,536,1,0,0,0,536,73,1,0,0,0,537,538,3,76,
        38,0,538,539,5,94,0,0,539,75,1,0,0,0,540,541,3,78,39,0,541,77,1,
        0,0,0,542,547,3,80,40,0,543,544,7,3,0,0,544,546,3,80,40,0,545,543,
        1,0,0,0,546,549,1,0,0,0,547,545,1,0,0,0,547,548,1,0,0,0,548,79,1,
        0,0,0,549,547,1,0,0,0,550,555,3,82,41,0,551,552,5,50,0,0,552,554,
        3,82,41,0,553,551,1,0,0,0,554,557,1,0,0,0,555,553,1,0,0,0,555,556,
        1,0,0,0,556,81,1,0,0,0,557,555,1,0,0,0,558,563,3,84,42,0,559,560,
        5,51,0,0,560,562,3,84,42,0,561,559,1,0,0,0,562,565,1,0,0,0,563,561,
        1,0,0,0,563,564,1,0,0,0,564,83,1,0,0,0,565,563,1,0,0,0,566,572,3,
        88,44,0,567,568,3,86,43,0,568,569,3,88,44,0,569,571,1,0,0,0,570,
        567,1,0,0,0,571,574,1,0,0,0,572,570,1,0,0,0,572,573,1,0,0,0,573,
        85,1,0,0,0,574,572,1,0,0,0,575,576,7,4,0,0,576,87,1,0,0,0,577,583,
        3,92,46,0,578,579,3,90,45,0,579,580,3,92,46,0,580,582,1,0,0,0,581,
        578,1,0,0,0,582,585,1,0,0,0,583,581,1,0,0,0,583,584,1,0,0,0,584,
        89,1,0,0,0,585,583,1,0,0,0,586,587,7,5,0,0,587,91,1,0,0,0,588,594,
        3,96,48,0,589,590,3,94,47,0,590,591,3,96,48,0,591,593,1,0,0,0,592,
        589,1,0,0,0,593,596,1,0,0,0,594,592,1,0,0,0,594,595,1,0,0,0,595,
        93,1,0,0,0,596,594,1,0,0,0,597,598,7,6,0,0,598,95,1,0,0,0,599,600,
        7,7,0,0,600,605,3,96,48,0,601,602,7,8,0,0,602,605,3,96,48,0,603,
        605,3,98,49,0,604,599,1,0,0,0,604,601,1,0,0,0,604,603,1,0,0,0,605,
        97,1,0,0,0,606,630,3,100,50,0,607,608,5,105,0,0,608,609,5,109,0,
        0,609,610,5,106,0,0,610,612,5,99,0,0,611,613,3,110,55,0,612,611,
        1,0,0,0,612,613,1,0,0,0,613,614,1,0,0,0,614,629,5,100,0,0,615,617,
        5,99,0,0,616,618,3,110,55,0,617,616,1,0,0,0,617,618,1,0,0,0,618,
        619,1,0,0,0,619,629,5,100,0,0,620,621,5,93,0,0,621,629,5,109,0,0,
        622,623,5,60,0,0,623,629,5,109,0,0,624,625,5,101,0,0,625,626,3,76,
        38,0,626,627,5,102,0,0,627,629,1,0,0,0,628,607,1,0,0,0,628,615,1,
        0,0,0,628,620,1,0,0,0,628,622,1,0,0,0,628,624,1,0,0,0,629,632,1,
        0,0,0,630,628,1,0,0,0,630,631,1,0,0,0,631,99,1,0,0,0,632,630,1,0,
        0,0,633,664,5,107,0,0,634,664,5,108,0,0,635,664,5,63,0,0,636,664,
        5,64,0,0,637,664,5,65,0,0,638,664,5,45,0,0,639,640,5,49,0,0,640,
        641,5,109,0,0,641,643,5,99,0,0,642,644,3,110,55,0,643,642,1,0,0,
        0,643,644,1,0,0,0,644,645,1,0,0,0,645,664,5,100,0,0,646,664,5,109,
        0,0,647,648,5,99,0,0,648,649,3,76,38,0,649,650,5,100,0,0,650,664,
        1,0,0,0,651,652,5,101,0,0,652,653,3,102,51,0,653,654,5,102,0,0,654,
        664,1,0,0,0,655,657,5,101,0,0,656,658,3,110,55,0,657,656,1,0,0,0,
        657,658,1,0,0,0,658,659,1,0,0,0,659,664,5,102,0,0,660,661,5,105,
        0,0,661,662,5,109,0,0,662,664,5,106,0,0,663,633,1,0,0,0,663,634,
        1,0,0,0,663,635,1,0,0,0,663,636,1,0,0,0,663,637,1,0,0,0,663,638,
        1,0,0,0,663,639,1,0,0,0,663,646,1,0,0,0,663,647,1,0,0,0,663,651,
        1,0,0,0,663,655,1,0,0,0,663,660,1,0,0,0,664,101,1,0,0,0,665,670,
        3,104,52,0,666,667,5,95,0,0,667,669,3,104,52,0,668,666,1,0,0,0,669,
        672,1,0,0,0,670,668,1,0,0,0,670,671,1,0,0,0,671,103,1,0,0,0,672,
        670,1,0,0,0,673,674,3,76,38,0,674,675,5,96,0,0,675,676,3,76,38,0,
        676,105,1,0,0,0,677,680,3,108,54,0,678,680,5,109,0,0,679,677,1,0,
        0,0,679,678,1,0,0,0,680,107,1,0,0,0,681,682,7,9,0,0,682,109,1,0,
        0,0,683,688,3,76,38,0,684,685,5,95,0,0,685,687,3,76,38,0,686,684,
        1,0,0,0,687,690,1,0,0,0,688,686,1,0,0,0,688,689,1,0,0,0,689,111,
        1,0,0,0,690,688,1,0,0,0,86,117,119,133,139,143,149,154,162,165,173,
        176,182,187,195,204,210,214,220,225,230,236,242,246,249,259,262,
        268,273,279,284,287,294,300,304,309,320,324,330,340,344,351,356,
        358,365,368,375,381,388,395,409,418,426,428,434,445,458,464,468,
        478,489,495,499,503,506,510,514,525,530,535,547,555,563,572,583,
        594,604,612,617,628,630,643,657,663,670,679,688
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
                     "'\\u5927\\u4E8E'", "'\\u5C0F\\u4E8E'", "'\\u8BBE'", 
                     "'\\u4E3A'", "'\\u5B9A\\u4E49'", "'\\u7B49\\u4E8E'", 
                     "'\\u6BB5\\u843D'", "'\\u63A5\\u6536'", "'\\u6570\\u636E\\u7C7B\\u578B'", 
                     "'\\u9519\\u8BEF'", "'\\u5E38\\u91CF'", "'\\u7C7B\\u578B'", 
                     "'\\u5BFC\\u51FA'", "'\\u5BFC\\u5165'", "'\\u4ECE'", 
                     "'\\u904D\\u5386'", "'\\u5F53'", "'\\u8DF3\\u51FA'", 
                     "'\\u8DF3\\u8FC7'", "'\\u5C1D\\u8BD5'", "'\\u6355\\u83B7'", 
                     "'\\u629B\\u51FA'", "'\\u8FD4\\u56DE'", "'\\u6253\\u5370'", 
                     "'\\u8F93\\u51FA'", "'\\u8F93\\u5165'", "'\\u7C7B'", 
                     "'\\u63A5\\u53E3'", "'\\u7EE7\\u627F'", "'\\u5B9E\\u73B0'", 
                     "'\\u4F7F\\u7528'", "'\\u7236'", "'\\u5DF1'", "'\\u65B9\\u6CD5'", 
                     "'\\u5C5E\\u6027'", "'\\u6784\\u9020'", "'\\u65B0\\u5EFA'", 
                     "'\\u4E14'", "'\\u6216'", "'\\u975E'", "'\\u52A0'", 
                     "'\\u51CF'", "'\\u4E58'", "'\\u9664'", "'\\u6A21'", 
                     "'\\u5E42'", "'\\u5E76'", "'\\u4E4B'", "'\\u4E8E'", 
                     "'\\u7684'", "'\\u771F'", "'\\u5047'", "'\\u7A7A'", 
                     "'\\u6570'", "'\\u6574\\u6570'", "'\\u6D6E\\u6570'", 
                     "'\\u4E32'", "'\\u5217'", "'\\u5178'", "'\\u96C6'", 
                     "'\\u5E03\\u5C14'", "'\\u4EFB\\u610F'", "'^'", "'%'", 
                     "<INVALID>", "<INVALID>", "'+'", "'-'", "'=='", "'!='", 
                     "'>='", "'<='", "'>'", "'<'", "'='", "'!'", "'&&'", 
                     "'||'", "'->'", "<INVALID>", "'.'", "'\\u3002'", "<INVALID>", 
                     "<INVALID>", "<INVALID>", "'\\u3001'", "<INVALID>", 
                     "<INVALID>", "<INVALID>", "<INVALID>", "'{'", "'}'", 
                     "'\\u300A'", "'\\u300B'" ]

    symbolicNames = [ "<INVALID>", "LINE_COMMENT", "COMMENT_START", "COMMENT_CLOSE", 
                      "COMMENT_CONTENT", "K_ELSE_IF", "K_IF", "K_THEN", 
                      "K_ELSE", "K_END", "K_GE", "K_LE", "K_NE", "K_GT", 
                      "K_LT", "K_SET", "K_AS", "K_DEFINE", "K_EQUAL", "K_SEGMENT", 
                      "K_RECEIVE", "K_DATA_TYPE", "K_ERROR_TYPE", "K_CONST", 
                      "K_TYPE", "K_EXPORT", "K_IMPORT", "K_FROM", "K_FOREACH", 
                      "K_WHILE", "K_BREAK", "K_CONTINUE", "K_TRY", "K_CATCH", 
                      "K_THROW", "K_RETURN", "K_PRINT", "K_OUTPUT", "K_INPUT", 
                      "K_CLASS", "K_INTERFACE", "K_INHERIT", "K_IMPLEMENTS", 
                      "K_USE", "K_PARENT", "K_SELF", "K_METHOD", "K_ATTRIBUTE", 
                      "K_CONSTRUCTOR", "K_NEW", "K_AND", "K_OR", "K_NOT", 
                      "K_PLUS", "K_MINUS", "K_MULTIPLY", "K_DIVIDE", "K_MOD", 
                      "K_POW", "K_AND_WORD", "K_OF", "K_AT", "K_DE", "K_TRUE", 
                      "K_FALSE", "K_NULL", "T_NUMBER", "T_INT", "T_FLOAT", 
                      "T_STRING", "T_LIST", "T_DICT", "T_SET", "T_BOOL", 
                      "T_ANY", "POW", "MODULO", "MULTIPLY", "DIVIDE", "PLUS", 
                      "MINUS", "EQ", "NE", "GE", "LE", "GT", "LT", "ASSIGN", 
                      "NOT", "AND", "OR", "PIPE", "PATH_SEP", "DOT", "PERIOD", 
                      "COMMA", "COLON", "SEMICOLON", "PAUSE", "LPAREN", 
                      "RPAREN", "LBRACKET", "RBRACKET", "LBRACE", "RBRACE", 
                      "BOOK_L", "BOOK_R", "NUMBER", "STRING", "ID", "NEWLINE", 
                      "WS", "UNKNOWN" ]

    RULE_program = 0
    RULE_moduleDecl = 1
    RULE_definition = 2
    RULE_paragraphDef = 3
    RULE_classDef = 4
    RULE_genericParams = 5
    RULE_classMember = 6
    RULE_methodDef = 7
    RULE_constructorDef = 8
    RULE_attributeDecl = 9
    RULE_interfaceDef = 10
    RULE_interfaceMember = 11
    RULE_paramList = 12
    RULE_param = 13
    RULE_block = 14
    RULE_dataTypeDef = 15
    RULE_dataTypeField = 16
    RULE_errorTypeDef = 17
    RULE_importStmt = 18
    RULE_exportStmt = 19
    RULE_path = 20
    RULE_importList = 21
    RULE_importItem = 22
    RULE_stmt = 23
    RULE_varDecl = 24
    RULE_assignStmt = 25
    RULE_target = 26
    RULE_ifStmt = 27
    RULE_foreachStmt = 28
    RULE_foreachVar = 29
    RULE_whileStmt = 30
    RULE_returnStmt = 31
    RULE_breakStmt = 32
    RULE_continueStmt = 33
    RULE_tryStmt = 34
    RULE_throwStmt = 35
    RULE_printStmt = 36
    RULE_exprStmt = 37
    RULE_expr = 38
    RULE_pipelineExpr = 39
    RULE_andExpr = 40
    RULE_orExpr = 41
    RULE_comparisonExpr = 42
    RULE_compOp = 43
    RULE_additiveExpr = 44
    RULE_addOp = 45
    RULE_multiplicativeExpr = 46
    RULE_multOp = 47
    RULE_unaryExpr = 48
    RULE_postfixExpr = 49
    RULE_primary = 50
    RULE_dictLiteral = 51
    RULE_dictEntry = 52
    RULE_typeAnnotation = 53
    RULE_builtinType = 54
    RULE_exprList = 55

    ruleNames =  [ "program", "moduleDecl", "definition", "paragraphDef", 
                   "classDef", "genericParams", "classMember", "methodDef", 
                   "constructorDef", "attributeDecl", "interfaceDef", "interfaceMember", 
                   "paramList", "param", "block", "dataTypeDef", "dataTypeField", 
                   "errorTypeDef", "importStmt", "exportStmt", "path", "importList", 
                   "importItem", "stmt", "varDecl", "assignStmt", "target", 
                   "ifStmt", "foreachStmt", "foreachVar", "whileStmt", "returnStmt", 
                   "breakStmt", "continueStmt", "tryStmt", "throwStmt", 
                   "printStmt", "exprStmt", "expr", "pipelineExpr", "andExpr", 
                   "orExpr", "comparisonExpr", "compOp", "additiveExpr", 
                   "addOp", "multiplicativeExpr", "multOp", "unaryExpr", 
                   "postfixExpr", "primary", "dictLiteral", "dictEntry", 
                   "typeAnnotation", "builtinType", "exprList" ]

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
    K_SET=15
    K_AS=16
    K_DEFINE=17
    K_EQUAL=18
    K_SEGMENT=19
    K_RECEIVE=20
    K_DATA_TYPE=21
    K_ERROR_TYPE=22
    K_CONST=23
    K_TYPE=24
    K_EXPORT=25
    K_IMPORT=26
    K_FROM=27
    K_FOREACH=28
    K_WHILE=29
    K_BREAK=30
    K_CONTINUE=31
    K_TRY=32
    K_CATCH=33
    K_THROW=34
    K_RETURN=35
    K_PRINT=36
    K_OUTPUT=37
    K_INPUT=38
    K_CLASS=39
    K_INTERFACE=40
    K_INHERIT=41
    K_IMPLEMENTS=42
    K_USE=43
    K_PARENT=44
    K_SELF=45
    K_METHOD=46
    K_ATTRIBUTE=47
    K_CONSTRUCTOR=48
    K_NEW=49
    K_AND=50
    K_OR=51
    K_NOT=52
    K_PLUS=53
    K_MINUS=54
    K_MULTIPLY=55
    K_DIVIDE=56
    K_MOD=57
    K_POW=58
    K_AND_WORD=59
    K_OF=60
    K_AT=61
    K_DE=62
    K_TRUE=63
    K_FALSE=64
    K_NULL=65
    T_NUMBER=66
    T_INT=67
    T_FLOAT=68
    T_STRING=69
    T_LIST=70
    T_DICT=71
    T_SET=72
    T_BOOL=73
    T_ANY=74
    POW=75
    MODULO=76
    MULTIPLY=77
    DIVIDE=78
    PLUS=79
    MINUS=80
    EQ=81
    NE=82
    GE=83
    LE=84
    GT=85
    LT=86
    ASSIGN=87
    NOT=88
    AND=89
    OR=90
    PIPE=91
    PATH_SEP=92
    DOT=93
    PERIOD=94
    COMMA=95
    COLON=96
    SEMICOLON=97
    PAUSE=98
    LPAREN=99
    RPAREN=100
    LBRACKET=101
    RBRACKET=102
    LBRACE=103
    RBRACE=104
    BOOK_L=105
    BOOK_R=106
    NUMBER=107
    STRING=108
    ID=109
    NEWLINE=110
    WS=111
    UNKNOWN=112

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

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterProgram" ):
                listener.enterProgram(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitProgram" ):
                listener.exitProgram(self)

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
            self.state = 119
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while (((_la) & ~0x3f) == 0 and ((1 << _la) & -9200253988869865408) != 0) or ((((_la - 64)) & ~0x3f) == 0 and ((1 << (_la - 64)) & 63943489945603) != 0):
                self.state = 117
                self._errHandler.sync(self)
                la_ = self._interp.adaptivePredict(self._input,0,self._ctx)
                if la_ == 1:
                    self.state = 112
                    self.moduleDecl()
                    pass

                elif la_ == 2:
                    self.state = 113
                    self.importStmt()
                    pass

                elif la_ == 3:
                    self.state = 114
                    self.exportStmt()
                    pass

                elif la_ == 4:
                    self.state = 115
                    self.definition()
                    pass

                elif la_ == 5:
                    self.state = 116
                    self.stmt()
                    pass


                self.state = 121
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 122
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

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterModuleDecl" ):
                listener.enterModuleDecl(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitModuleDecl" ):
                listener.exitModuleDecl(self)

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
            self.state = 124
            self.match(DuanLangParser.LBRACKET)
            self.state = 125
            self.match(DuanLangParser.ID)
            self.state = 126
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


        def classDef(self):
            return self.getTypedRuleContext(DuanLangParser.ClassDefContext,0)


        def interfaceDef(self):
            return self.getTypedRuleContext(DuanLangParser.InterfaceDefContext,0)


        def dataTypeDef(self):
            return self.getTypedRuleContext(DuanLangParser.DataTypeDefContext,0)


        def errorTypeDef(self):
            return self.getTypedRuleContext(DuanLangParser.ErrorTypeDefContext,0)


        def getRuleIndex(self):
            return DuanLangParser.RULE_definition

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterDefinition" ):
                listener.enterDefinition(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitDefinition" ):
                listener.exitDefinition(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitDefinition" ):
                return visitor.visitDefinition(self)
            else:
                return visitor.visitChildren(self)




    def definition(self):

        localctx = DuanLangParser.DefinitionContext(self, self._ctx, self.state)
        self.enterRule(localctx, 4, self.RULE_definition)
        try:
            self.state = 133
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,2,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 128
                self.paragraphDef()
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 129
                self.classDef()
                pass

            elif la_ == 3:
                self.enterOuterAlt(localctx, 3)
                self.state = 130
                self.interfaceDef()
                pass

            elif la_ == 4:
                self.enterOuterAlt(localctx, 4)
                self.state = 131
                self.dataTypeDef()
                pass

            elif la_ == 5:
                self.enterOuterAlt(localctx, 5)
                self.state = 132
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

        def K_SEGMENT(self):
            return self.getToken(DuanLangParser.K_SEGMENT, 0)

        def ID(self):
            return self.getToken(DuanLangParser.ID, 0)

        def COLON(self):
            return self.getToken(DuanLangParser.COLON, 0)

        def block(self):
            return self.getTypedRuleContext(DuanLangParser.BlockContext,0)


        def K_END(self):
            return self.getToken(DuanLangParser.K_END, 0)

        def K_RECEIVE(self):
            return self.getToken(DuanLangParser.K_RECEIVE, 0)

        def paramList(self):
            return self.getTypedRuleContext(DuanLangParser.ParamListContext,0)


        def K_RETURN(self):
            return self.getToken(DuanLangParser.K_RETURN, 0)

        def typeAnnotation(self):
            return self.getTypedRuleContext(DuanLangParser.TypeAnnotationContext,0)


        def PERIOD(self):
            return self.getToken(DuanLangParser.PERIOD, 0)

        def getRuleIndex(self):
            return DuanLangParser.RULE_paragraphDef

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterParagraphDef" ):
                listener.enterParagraphDef(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitParagraphDef" ):
                listener.exitParagraphDef(self)

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
            self.state = 135
            self.match(DuanLangParser.K_SEGMENT)
            self.state = 136
            self.match(DuanLangParser.ID)
            self.state = 139
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==20:
                self.state = 137
                self.match(DuanLangParser.K_RECEIVE)
                self.state = 138
                self.paramList()


            self.state = 143
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==35:
                self.state = 141
                self.match(DuanLangParser.K_RETURN)
                self.state = 142
                self.typeAnnotation()


            self.state = 145
            self.match(DuanLangParser.COLON)
            self.state = 146
            self.block()
            self.state = 147
            self.match(DuanLangParser.K_END)
            self.state = 149
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==94:
                self.state = 148
                self.match(DuanLangParser.PERIOD)


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ClassDefContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def K_CLASS(self):
            return self.getToken(DuanLangParser.K_CLASS, 0)

        def ID(self):
            return self.getToken(DuanLangParser.ID, 0)

        def COLON(self):
            return self.getToken(DuanLangParser.COLON, 0)

        def K_END(self):
            return self.getToken(DuanLangParser.K_END, 0)

        def genericParams(self):
            return self.getTypedRuleContext(DuanLangParser.GenericParamsContext,0)


        def K_INHERIT(self):
            return self.getToken(DuanLangParser.K_INHERIT, 0)

        def typeAnnotation(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(DuanLangParser.TypeAnnotationContext)
            else:
                return self.getTypedRuleContext(DuanLangParser.TypeAnnotationContext,i)


        def K_IMPLEMENTS(self):
            return self.getToken(DuanLangParser.K_IMPLEMENTS, 0)

        def classMember(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(DuanLangParser.ClassMemberContext)
            else:
                return self.getTypedRuleContext(DuanLangParser.ClassMemberContext,i)


        def PERIOD(self):
            return self.getToken(DuanLangParser.PERIOD, 0)

        def COMMA(self, i:int=None):
            if i is None:
                return self.getTokens(DuanLangParser.COMMA)
            else:
                return self.getToken(DuanLangParser.COMMA, i)

        def getRuleIndex(self):
            return DuanLangParser.RULE_classDef

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterClassDef" ):
                listener.enterClassDef(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitClassDef" ):
                listener.exitClassDef(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitClassDef" ):
                return visitor.visitClassDef(self)
            else:
                return visitor.visitChildren(self)




    def classDef(self):

        localctx = DuanLangParser.ClassDefContext(self, self._ctx, self.state)
        self.enterRule(localctx, 8, self.RULE_classDef)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 151
            self.match(DuanLangParser.K_CLASS)
            self.state = 152
            self.match(DuanLangParser.ID)
            self.state = 154
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==101:
                self.state = 153
                self.genericParams()


            self.state = 165
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==41:
                self.state = 156
                self.match(DuanLangParser.K_INHERIT)
                self.state = 157
                self.typeAnnotation()
                self.state = 162
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                while _la==95:
                    self.state = 158
                    self.match(DuanLangParser.COMMA)
                    self.state = 159
                    self.typeAnnotation()
                    self.state = 164
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)



            self.state = 176
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==42:
                self.state = 167
                self.match(DuanLangParser.K_IMPLEMENTS)
                self.state = 168
                self.typeAnnotation()
                self.state = 173
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                while _la==95:
                    self.state = 169
                    self.match(DuanLangParser.COMMA)
                    self.state = 170
                    self.typeAnnotation()
                    self.state = 175
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)



            self.state = 178
            self.match(DuanLangParser.COLON)
            self.state = 182
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while (((_la) & ~0x3f) == 0 and ((1 << _la) & -9199833425907122112) != 0) or ((((_la - 64)) & ~0x3f) == 0 and ((1 << (_la - 64)) & 63943489945603) != 0):
                self.state = 179
                self.classMember()
                self.state = 184
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 185
            self.match(DuanLangParser.K_END)
            self.state = 187
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==94:
                self.state = 186
                self.match(DuanLangParser.PERIOD)


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class GenericParamsContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def LBRACKET(self):
            return self.getToken(DuanLangParser.LBRACKET, 0)

        def ID(self, i:int=None):
            if i is None:
                return self.getTokens(DuanLangParser.ID)
            else:
                return self.getToken(DuanLangParser.ID, i)

        def RBRACKET(self):
            return self.getToken(DuanLangParser.RBRACKET, 0)

        def COMMA(self, i:int=None):
            if i is None:
                return self.getTokens(DuanLangParser.COMMA)
            else:
                return self.getToken(DuanLangParser.COMMA, i)

        def getRuleIndex(self):
            return DuanLangParser.RULE_genericParams

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterGenericParams" ):
                listener.enterGenericParams(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitGenericParams" ):
                listener.exitGenericParams(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitGenericParams" ):
                return visitor.visitGenericParams(self)
            else:
                return visitor.visitChildren(self)




    def genericParams(self):

        localctx = DuanLangParser.GenericParamsContext(self, self._ctx, self.state)
        self.enterRule(localctx, 10, self.RULE_genericParams)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 189
            self.match(DuanLangParser.LBRACKET)
            self.state = 190
            self.match(DuanLangParser.ID)
            self.state = 195
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==95:
                self.state = 191
                self.match(DuanLangParser.COMMA)
                self.state = 192
                self.match(DuanLangParser.ID)
                self.state = 197
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 198
            self.match(DuanLangParser.RBRACKET)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ClassMemberContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def methodDef(self):
            return self.getTypedRuleContext(DuanLangParser.MethodDefContext,0)


        def constructorDef(self):
            return self.getTypedRuleContext(DuanLangParser.ConstructorDefContext,0)


        def attributeDecl(self):
            return self.getTypedRuleContext(DuanLangParser.AttributeDeclContext,0)


        def stmt(self):
            return self.getTypedRuleContext(DuanLangParser.StmtContext,0)


        def getRuleIndex(self):
            return DuanLangParser.RULE_classMember

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterClassMember" ):
                listener.enterClassMember(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitClassMember" ):
                listener.exitClassMember(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitClassMember" ):
                return visitor.visitClassMember(self)
            else:
                return visitor.visitChildren(self)




    def classMember(self):

        localctx = DuanLangParser.ClassMemberContext(self, self._ctx, self.state)
        self.enterRule(localctx, 12, self.RULE_classMember)
        try:
            self.state = 204
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [19]:
                self.enterOuterAlt(localctx, 1)
                self.state = 200
                self.methodDef()
                pass
            elif token in [48]:
                self.enterOuterAlt(localctx, 2)
                self.state = 201
                self.constructorDef()
                pass
            elif token in [47]:
                self.enterOuterAlt(localctx, 3)
                self.state = 202
                self.attributeDecl()
                pass
            elif token in [6, 15, 17, 28, 29, 30, 31, 32, 34, 35, 36, 37, 45, 49, 52, 54, 63, 64, 65, 80, 88, 99, 101, 105, 107, 108, 109]:
                self.enterOuterAlt(localctx, 4)
                self.state = 203
                self.stmt()
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


    class MethodDefContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def K_SEGMENT(self):
            return self.getToken(DuanLangParser.K_SEGMENT, 0)

        def ID(self):
            return self.getToken(DuanLangParser.ID, 0)

        def COLON(self):
            return self.getToken(DuanLangParser.COLON, 0)

        def block(self):
            return self.getTypedRuleContext(DuanLangParser.BlockContext,0)


        def K_END(self):
            return self.getToken(DuanLangParser.K_END, 0)

        def K_RECEIVE(self):
            return self.getToken(DuanLangParser.K_RECEIVE, 0)

        def paramList(self):
            return self.getTypedRuleContext(DuanLangParser.ParamListContext,0)


        def K_RETURN(self):
            return self.getToken(DuanLangParser.K_RETURN, 0)

        def typeAnnotation(self):
            return self.getTypedRuleContext(DuanLangParser.TypeAnnotationContext,0)


        def PERIOD(self):
            return self.getToken(DuanLangParser.PERIOD, 0)

        def getRuleIndex(self):
            return DuanLangParser.RULE_methodDef

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterMethodDef" ):
                listener.enterMethodDef(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitMethodDef" ):
                listener.exitMethodDef(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitMethodDef" ):
                return visitor.visitMethodDef(self)
            else:
                return visitor.visitChildren(self)




    def methodDef(self):

        localctx = DuanLangParser.MethodDefContext(self, self._ctx, self.state)
        self.enterRule(localctx, 14, self.RULE_methodDef)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 206
            self.match(DuanLangParser.K_SEGMENT)
            self.state = 207
            self.match(DuanLangParser.ID)
            self.state = 210
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==20:
                self.state = 208
                self.match(DuanLangParser.K_RECEIVE)
                self.state = 209
                self.paramList()


            self.state = 214
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==35:
                self.state = 212
                self.match(DuanLangParser.K_RETURN)
                self.state = 213
                self.typeAnnotation()


            self.state = 216
            self.match(DuanLangParser.COLON)
            self.state = 217
            self.block()
            self.state = 218
            self.match(DuanLangParser.K_END)
            self.state = 220
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==94:
                self.state = 219
                self.match(DuanLangParser.PERIOD)


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ConstructorDefContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def K_CONSTRUCTOR(self):
            return self.getToken(DuanLangParser.K_CONSTRUCTOR, 0)

        def COLON(self):
            return self.getToken(DuanLangParser.COLON, 0)

        def block(self):
            return self.getTypedRuleContext(DuanLangParser.BlockContext,0)


        def K_END(self):
            return self.getToken(DuanLangParser.K_END, 0)

        def LPAREN(self):
            return self.getToken(DuanLangParser.LPAREN, 0)

        def RPAREN(self):
            return self.getToken(DuanLangParser.RPAREN, 0)

        def K_RECEIVE(self):
            return self.getToken(DuanLangParser.K_RECEIVE, 0)

        def paramList(self):
            return self.getTypedRuleContext(DuanLangParser.ParamListContext,0)


        def PERIOD(self):
            return self.getToken(DuanLangParser.PERIOD, 0)

        def getRuleIndex(self):
            return DuanLangParser.RULE_constructorDef

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterConstructorDef" ):
                listener.enterConstructorDef(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitConstructorDef" ):
                listener.exitConstructorDef(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitConstructorDef" ):
                return visitor.visitConstructorDef(self)
            else:
                return visitor.visitChildren(self)




    def constructorDef(self):

        localctx = DuanLangParser.ConstructorDefContext(self, self._ctx, self.state)
        self.enterRule(localctx, 16, self.RULE_constructorDef)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 222
            self.match(DuanLangParser.K_CONSTRUCTOR)
            self.state = 230
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [99]:
                self.state = 223
                self.match(DuanLangParser.LPAREN)
                self.state = 225
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la==109:
                    self.state = 224
                    self.paramList()


                self.state = 227
                self.match(DuanLangParser.RPAREN)
                pass
            elif token in [20]:
                self.state = 228
                self.match(DuanLangParser.K_RECEIVE)
                self.state = 229
                self.paramList()
                pass
            elif token in [96]:
                pass
            else:
                pass
            self.state = 232
            self.match(DuanLangParser.COLON)
            self.state = 233
            self.block()
            self.state = 234
            self.match(DuanLangParser.K_END)
            self.state = 236
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==94:
                self.state = 235
                self.match(DuanLangParser.PERIOD)


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class AttributeDeclContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def K_ATTRIBUTE(self):
            return self.getToken(DuanLangParser.K_ATTRIBUTE, 0)

        def ID(self):
            return self.getToken(DuanLangParser.ID, 0)

        def K_AS(self):
            return self.getToken(DuanLangParser.K_AS, 0)

        def typeAnnotation(self):
            return self.getTypedRuleContext(DuanLangParser.TypeAnnotationContext,0)


        def K_EQUAL(self):
            return self.getToken(DuanLangParser.K_EQUAL, 0)

        def expr(self):
            return self.getTypedRuleContext(DuanLangParser.ExprContext,0)


        def PERIOD(self):
            return self.getToken(DuanLangParser.PERIOD, 0)

        def getRuleIndex(self):
            return DuanLangParser.RULE_attributeDecl

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterAttributeDecl" ):
                listener.enterAttributeDecl(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitAttributeDecl" ):
                listener.exitAttributeDecl(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitAttributeDecl" ):
                return visitor.visitAttributeDecl(self)
            else:
                return visitor.visitChildren(self)




    def attributeDecl(self):

        localctx = DuanLangParser.AttributeDeclContext(self, self._ctx, self.state)
        self.enterRule(localctx, 18, self.RULE_attributeDecl)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 238
            self.match(DuanLangParser.K_ATTRIBUTE)
            self.state = 239
            self.match(DuanLangParser.ID)
            self.state = 242
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==16:
                self.state = 240
                self.match(DuanLangParser.K_AS)
                self.state = 241
                self.typeAnnotation()


            self.state = 246
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==18:
                self.state = 244
                self.match(DuanLangParser.K_EQUAL)
                self.state = 245
                self.expr()


            self.state = 249
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==94:
                self.state = 248
                self.match(DuanLangParser.PERIOD)


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class InterfaceDefContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def K_INTERFACE(self):
            return self.getToken(DuanLangParser.K_INTERFACE, 0)

        def ID(self):
            return self.getToken(DuanLangParser.ID, 0)

        def COLON(self):
            return self.getToken(DuanLangParser.COLON, 0)

        def K_END(self):
            return self.getToken(DuanLangParser.K_END, 0)

        def K_INHERIT(self):
            return self.getToken(DuanLangParser.K_INHERIT, 0)

        def typeAnnotation(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(DuanLangParser.TypeAnnotationContext)
            else:
                return self.getTypedRuleContext(DuanLangParser.TypeAnnotationContext,i)


        def interfaceMember(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(DuanLangParser.InterfaceMemberContext)
            else:
                return self.getTypedRuleContext(DuanLangParser.InterfaceMemberContext,i)


        def PERIOD(self):
            return self.getToken(DuanLangParser.PERIOD, 0)

        def COMMA(self, i:int=None):
            if i is None:
                return self.getTokens(DuanLangParser.COMMA)
            else:
                return self.getToken(DuanLangParser.COMMA, i)

        def getRuleIndex(self):
            return DuanLangParser.RULE_interfaceDef

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterInterfaceDef" ):
                listener.enterInterfaceDef(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitInterfaceDef" ):
                listener.exitInterfaceDef(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitInterfaceDef" ):
                return visitor.visitInterfaceDef(self)
            else:
                return visitor.visitChildren(self)




    def interfaceDef(self):

        localctx = DuanLangParser.InterfaceDefContext(self, self._ctx, self.state)
        self.enterRule(localctx, 20, self.RULE_interfaceDef)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 251
            self.match(DuanLangParser.K_INTERFACE)
            self.state = 252
            self.match(DuanLangParser.ID)
            self.state = 262
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==41:
                self.state = 253
                self.match(DuanLangParser.K_INHERIT)
                self.state = 254
                self.typeAnnotation()
                self.state = 259
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                while _la==95:
                    self.state = 255
                    self.match(DuanLangParser.COMMA)
                    self.state = 256
                    self.typeAnnotation()
                    self.state = 261
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)



            self.state = 264
            self.match(DuanLangParser.COLON)
            self.state = 268
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==46:
                self.state = 265
                self.interfaceMember()
                self.state = 270
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 271
            self.match(DuanLangParser.K_END)
            self.state = 273
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==94:
                self.state = 272
                self.match(DuanLangParser.PERIOD)


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class InterfaceMemberContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def K_METHOD(self):
            return self.getToken(DuanLangParser.K_METHOD, 0)

        def ID(self):
            return self.getToken(DuanLangParser.ID, 0)

        def LPAREN(self):
            return self.getToken(DuanLangParser.LPAREN, 0)

        def RPAREN(self):
            return self.getToken(DuanLangParser.RPAREN, 0)

        def paramList(self):
            return self.getTypedRuleContext(DuanLangParser.ParamListContext,0)


        def K_RETURN(self):
            return self.getToken(DuanLangParser.K_RETURN, 0)

        def typeAnnotation(self):
            return self.getTypedRuleContext(DuanLangParser.TypeAnnotationContext,0)


        def PERIOD(self):
            return self.getToken(DuanLangParser.PERIOD, 0)

        def getRuleIndex(self):
            return DuanLangParser.RULE_interfaceMember

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterInterfaceMember" ):
                listener.enterInterfaceMember(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitInterfaceMember" ):
                listener.exitInterfaceMember(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitInterfaceMember" ):
                return visitor.visitInterfaceMember(self)
            else:
                return visitor.visitChildren(self)




    def interfaceMember(self):

        localctx = DuanLangParser.InterfaceMemberContext(self, self._ctx, self.state)
        self.enterRule(localctx, 22, self.RULE_interfaceMember)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 275
            self.match(DuanLangParser.K_METHOD)
            self.state = 276
            self.match(DuanLangParser.ID)
            self.state = 277
            self.match(DuanLangParser.LPAREN)
            self.state = 279
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==109:
                self.state = 278
                self.paramList()


            self.state = 281
            self.match(DuanLangParser.RPAREN)
            self.state = 284
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==35:
                self.state = 282
                self.match(DuanLangParser.K_RETURN)
                self.state = 283
                self.typeAnnotation()


            self.state = 287
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==94:
                self.state = 286
                self.match(DuanLangParser.PERIOD)


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

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterParamList" ):
                listener.enterParamList(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitParamList" ):
                listener.exitParamList(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitParamList" ):
                return visitor.visitParamList(self)
            else:
                return visitor.visitChildren(self)




    def paramList(self):

        localctx = DuanLangParser.ParamListContext(self, self._ctx, self.state)
        self.enterRule(localctx, 24, self.RULE_paramList)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 289
            self.param()
            self.state = 294
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==95:
                self.state = 290
                self.match(DuanLangParser.COMMA)
                self.state = 291
                self.param()
                self.state = 296
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

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterParam" ):
                listener.enterParam(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitParam" ):
                listener.exitParam(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitParam" ):
                return visitor.visitParam(self)
            else:
                return visitor.visitChildren(self)




    def param(self):

        localctx = DuanLangParser.ParamContext(self, self._ctx, self.state)
        self.enterRule(localctx, 26, self.RULE_param)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 297
            self.match(DuanLangParser.ID)
            self.state = 300
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,32,self._ctx)
            if la_ == 1:
                self.state = 298
                self.match(DuanLangParser.COLON)
                self.state = 299
                self.typeAnnotation()


            self.state = 304
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==18:
                self.state = 302
                self.match(DuanLangParser.K_EQUAL)
                self.state = 303
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

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterBlock" ):
                listener.enterBlock(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitBlock" ):
                listener.exitBlock(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitBlock" ):
                return visitor.visitBlock(self)
            else:
                return visitor.visitChildren(self)




    def block(self):

        localctx = DuanLangParser.BlockContext(self, self._ctx, self.state)
        self.enterRule(localctx, 28, self.RULE_block)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 309
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while (((_la) & ~0x3f) == 0 and ((1 << _la) & -9200255638372712384) != 0) or ((((_la - 64)) & ~0x3f) == 0 and ((1 << (_la - 64)) & 63943489945603) != 0):
                self.state = 306
                self.stmt()
                self.state = 311
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


        def PERIOD(self):
            return self.getToken(DuanLangParser.PERIOD, 0)

        def getRuleIndex(self):
            return DuanLangParser.RULE_dataTypeDef

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterDataTypeDef" ):
                listener.enterDataTypeDef(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitDataTypeDef" ):
                listener.exitDataTypeDef(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitDataTypeDef" ):
                return visitor.visitDataTypeDef(self)
            else:
                return visitor.visitChildren(self)




    def dataTypeDef(self):

        localctx = DuanLangParser.DataTypeDefContext(self, self._ctx, self.state)
        self.enterRule(localctx, 30, self.RULE_dataTypeDef)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 312
            self.match(DuanLangParser.BOOK_L)
            self.state = 313
            self.match(DuanLangParser.ID)
            self.state = 314
            self.match(DuanLangParser.BOOK_R)
            self.state = 315
            self.match(DuanLangParser.K_DATA_TYPE)
            self.state = 316
            self.match(DuanLangParser.COLON)
            self.state = 318 
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while True:
                self.state = 317
                self.dataTypeField()
                self.state = 320 
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if not (_la==109):
                    break

            self.state = 322
            self.match(DuanLangParser.K_END)
            self.state = 324
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==94:
                self.state = 323
                self.match(DuanLangParser.PERIOD)


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


        def PERIOD(self):
            return self.getToken(DuanLangParser.PERIOD, 0)

        def getRuleIndex(self):
            return DuanLangParser.RULE_dataTypeField

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterDataTypeField" ):
                listener.enterDataTypeField(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitDataTypeField" ):
                listener.exitDataTypeField(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitDataTypeField" ):
                return visitor.visitDataTypeField(self)
            else:
                return visitor.visitChildren(self)




    def dataTypeField(self):

        localctx = DuanLangParser.DataTypeFieldContext(self, self._ctx, self.state)
        self.enterRule(localctx, 32, self.RULE_dataTypeField)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 326
            self.match(DuanLangParser.ID)
            self.state = 327
            self.match(DuanLangParser.COLON)
            self.state = 328
            self.typeAnnotation()
            self.state = 330
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==94:
                self.state = 329
                self.match(DuanLangParser.PERIOD)


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


        def PERIOD(self):
            return self.getToken(DuanLangParser.PERIOD, 0)

        def getRuleIndex(self):
            return DuanLangParser.RULE_errorTypeDef

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterErrorTypeDef" ):
                listener.enterErrorTypeDef(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitErrorTypeDef" ):
                listener.exitErrorTypeDef(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitErrorTypeDef" ):
                return visitor.visitErrorTypeDef(self)
            else:
                return visitor.visitChildren(self)




    def errorTypeDef(self):

        localctx = DuanLangParser.ErrorTypeDefContext(self, self._ctx, self.state)
        self.enterRule(localctx, 34, self.RULE_errorTypeDef)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 332
            self.match(DuanLangParser.BOOK_L)
            self.state = 333
            self.match(DuanLangParser.ID)
            self.state = 334
            self.match(DuanLangParser.BOOK_R)
            self.state = 335
            self.match(DuanLangParser.K_ERROR_TYPE)
            self.state = 336
            self.match(DuanLangParser.COLON)
            self.state = 338 
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while True:
                self.state = 337
                self.dataTypeField()
                self.state = 340 
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if not (_la==109):
                    break

            self.state = 342
            self.match(DuanLangParser.K_END)
            self.state = 344
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==94:
                self.state = 343
                self.match(DuanLangParser.PERIOD)


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


        def PERIOD(self):
            return self.getToken(DuanLangParser.PERIOD, 0)

        def getRuleIndex(self):
            return DuanLangParser.RULE_importStmt

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterImportStmt" ):
                listener.enterImportStmt(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitImportStmt" ):
                listener.exitImportStmt(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitImportStmt" ):
                return visitor.visitImportStmt(self)
            else:
                return visitor.visitChildren(self)




    def importStmt(self):

        localctx = DuanLangParser.ImportStmtContext(self, self._ctx, self.state)
        self.enterRule(localctx, 36, self.RULE_importStmt)
        self._la = 0 # Token type
        try:
            self.state = 358
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [27]:
                self.enterOuterAlt(localctx, 1)
                self.state = 346
                self.match(DuanLangParser.K_FROM)
                self.state = 347
                self.path()
                self.state = 348
                self.match(DuanLangParser.K_IMPORT)
                self.state = 349
                self.importList()
                self.state = 351
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la==94:
                    self.state = 350
                    self.match(DuanLangParser.PERIOD)


                pass
            elif token in [26]:
                self.enterOuterAlt(localctx, 2)
                self.state = 353
                self.match(DuanLangParser.K_IMPORT)
                self.state = 354
                self.importList()
                self.state = 356
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la==94:
                    self.state = 355
                    self.match(DuanLangParser.PERIOD)


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

        def PERIOD(self):
            return self.getToken(DuanLangParser.PERIOD, 0)

        def getRuleIndex(self):
            return DuanLangParser.RULE_exportStmt

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterExportStmt" ):
                listener.enterExportStmt(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitExportStmt" ):
                listener.exitExportStmt(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitExportStmt" ):
                return visitor.visitExportStmt(self)
            else:
                return visitor.visitChildren(self)




    def exportStmt(self):

        localctx = DuanLangParser.ExportStmtContext(self, self._ctx, self.state)
        self.enterRule(localctx, 38, self.RULE_exportStmt)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 360
            self.match(DuanLangParser.K_EXPORT)
            self.state = 365
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [109]:
                self.state = 361
                self.match(DuanLangParser.ID)
                pass
            elif token in [105]:
                self.state = 362
                self.match(DuanLangParser.BOOK_L)
                self.state = 363
                self.match(DuanLangParser.ID)
                self.state = 364
                self.match(DuanLangParser.BOOK_R)
                pass
            else:
                raise NoViableAltException(self)

            self.state = 368
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==94:
                self.state = 367
                self.match(DuanLangParser.PERIOD)


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

        def BOOK_L(self):
            return self.getToken(DuanLangParser.BOOK_L, 0)

        def BOOK_R(self):
            return self.getToken(DuanLangParser.BOOK_R, 0)

        def getRuleIndex(self):
            return DuanLangParser.RULE_path

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterPath" ):
                listener.enterPath(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitPath" ):
                listener.exitPath(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitPath" ):
                return visitor.visitPath(self)
            else:
                return visitor.visitChildren(self)




    def path(self):

        localctx = DuanLangParser.PathContext(self, self._ctx, self.state)
        self.enterRule(localctx, 40, self.RULE_path)
        self._la = 0 # Token type
        try:
            self.state = 381
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [109]:
                self.enterOuterAlt(localctx, 1)
                self.state = 370
                self.match(DuanLangParser.ID)
                self.state = 375
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                while _la==92:
                    self.state = 371
                    self.match(DuanLangParser.PATH_SEP)
                    self.state = 372
                    self.match(DuanLangParser.ID)
                    self.state = 377
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)

                pass
            elif token in [105]:
                self.enterOuterAlt(localctx, 2)
                self.state = 378
                self.match(DuanLangParser.BOOK_L)
                self.state = 379
                self.match(DuanLangParser.ID)
                self.state = 380
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

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterImportList" ):
                listener.enterImportList(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitImportList" ):
                listener.exitImportList(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitImportList" ):
                return visitor.visitImportList(self)
            else:
                return visitor.visitChildren(self)




    def importList(self):

        localctx = DuanLangParser.ImportListContext(self, self._ctx, self.state)
        self.enterRule(localctx, 42, self.RULE_importList)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 383
            self.importItem()
            self.state = 388
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==95:
                self.state = 384
                self.match(DuanLangParser.COMMA)
                self.state = 385
                self.importItem()
                self.state = 390
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

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterImportItem" ):
                listener.enterImportItem(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitImportItem" ):
                listener.exitImportItem(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitImportItem" ):
                return visitor.visitImportItem(self)
            else:
                return visitor.visitChildren(self)




    def importItem(self):

        localctx = DuanLangParser.ImportItemContext(self, self._ctx, self.state)
        self.enterRule(localctx, 44, self.RULE_importItem)
        try:
            self.state = 395
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [105]:
                self.enterOuterAlt(localctx, 1)
                self.state = 391
                self.match(DuanLangParser.BOOK_L)
                self.state = 392
                self.match(DuanLangParser.ID)
                self.state = 393
                self.match(DuanLangParser.BOOK_R)
                pass
            elif token in [109]:
                self.enterOuterAlt(localctx, 2)
                self.state = 394
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

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterStmt" ):
                listener.enterStmt(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitStmt" ):
                listener.exitStmt(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitStmt" ):
                return visitor.visitStmt(self)
            else:
                return visitor.visitChildren(self)




    def stmt(self):

        localctx = DuanLangParser.StmtContext(self, self._ctx, self.state)
        self.enterRule(localctx, 46, self.RULE_stmt)
        try:
            self.state = 409
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,49,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 397
                self.varDecl()
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 398
                self.assignStmt()
                pass

            elif la_ == 3:
                self.enterOuterAlt(localctx, 3)
                self.state = 399
                self.ifStmt()
                pass

            elif la_ == 4:
                self.enterOuterAlt(localctx, 4)
                self.state = 400
                self.foreachStmt()
                pass

            elif la_ == 5:
                self.enterOuterAlt(localctx, 5)
                self.state = 401
                self.whileStmt()
                pass

            elif la_ == 6:
                self.enterOuterAlt(localctx, 6)
                self.state = 402
                self.returnStmt()
                pass

            elif la_ == 7:
                self.enterOuterAlt(localctx, 7)
                self.state = 403
                self.breakStmt()
                pass

            elif la_ == 8:
                self.enterOuterAlt(localctx, 8)
                self.state = 404
                self.continueStmt()
                pass

            elif la_ == 9:
                self.enterOuterAlt(localctx, 9)
                self.state = 405
                self.tryStmt()
                pass

            elif la_ == 10:
                self.enterOuterAlt(localctx, 10)
                self.state = 406
                self.throwStmt()
                pass

            elif la_ == 11:
                self.enterOuterAlt(localctx, 11)
                self.state = 407
                self.printStmt()
                pass

            elif la_ == 12:
                self.enterOuterAlt(localctx, 12)
                self.state = 408
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

        def K_SET(self):
            return self.getToken(DuanLangParser.K_SET, 0)

        def ID(self):
            return self.getToken(DuanLangParser.ID, 0)

        def K_AS(self):
            return self.getToken(DuanLangParser.K_AS, 0)

        def expr(self):
            return self.getTypedRuleContext(DuanLangParser.ExprContext,0)


        def PERIOD(self):
            return self.getToken(DuanLangParser.PERIOD, 0)

        def K_TYPE(self):
            return self.getToken(DuanLangParser.K_TYPE, 0)

        def typeAnnotation(self):
            return self.getTypedRuleContext(DuanLangParser.TypeAnnotationContext,0)


        def K_DEFINE(self):
            return self.getToken(DuanLangParser.K_DEFINE, 0)

        def K_EQUAL(self):
            return self.getToken(DuanLangParser.K_EQUAL, 0)

        def getRuleIndex(self):
            return DuanLangParser.RULE_varDecl

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterVarDecl" ):
                listener.enterVarDecl(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitVarDecl" ):
                listener.exitVarDecl(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitVarDecl" ):
                return visitor.visitVarDecl(self)
            else:
                return visitor.visitChildren(self)




    def varDecl(self):

        localctx = DuanLangParser.VarDeclContext(self, self._ctx, self.state)
        self.enterRule(localctx, 48, self.RULE_varDecl)
        self._la = 0 # Token type
        try:
            self.state = 428
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [15]:
                self.enterOuterAlt(localctx, 1)
                self.state = 411
                self.match(DuanLangParser.K_SET)
                self.state = 412
                self.match(DuanLangParser.ID)
                self.state = 413
                self.match(DuanLangParser.K_AS)
                self.state = 414
                self.expr()
                self.state = 415
                self.match(DuanLangParser.PERIOD)
                self.state = 418
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la==24:
                    self.state = 416
                    self.match(DuanLangParser.K_TYPE)
                    self.state = 417
                    self.typeAnnotation()


                pass
            elif token in [17]:
                self.enterOuterAlt(localctx, 2)
                self.state = 420
                self.match(DuanLangParser.K_DEFINE)
                self.state = 421
                self.match(DuanLangParser.ID)
                self.state = 426
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la==18:
                    self.state = 422
                    self.match(DuanLangParser.K_EQUAL)
                    self.state = 423
                    self.expr()
                    self.state = 424
                    self.match(DuanLangParser.PERIOD)


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


    class AssignStmtContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def target(self):
            return self.getTypedRuleContext(DuanLangParser.TargetContext,0)


        def expr(self):
            return self.getTypedRuleContext(DuanLangParser.ExprContext,0)


        def ASSIGN(self):
            return self.getToken(DuanLangParser.ASSIGN, 0)

        def K_EQUAL(self):
            return self.getToken(DuanLangParser.K_EQUAL, 0)

        def K_AS(self):
            return self.getToken(DuanLangParser.K_AS, 0)

        def PERIOD(self):
            return self.getToken(DuanLangParser.PERIOD, 0)

        def getRuleIndex(self):
            return DuanLangParser.RULE_assignStmt

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterAssignStmt" ):
                listener.enterAssignStmt(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitAssignStmt" ):
                listener.exitAssignStmt(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitAssignStmt" ):
                return visitor.visitAssignStmt(self)
            else:
                return visitor.visitChildren(self)




    def assignStmt(self):

        localctx = DuanLangParser.AssignStmtContext(self, self._ctx, self.state)
        self.enterRule(localctx, 50, self.RULE_assignStmt)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 430
            self.target()
            self.state = 431
            _la = self._input.LA(1)
            if not(_la==16 or _la==18 or _la==87):
                self._errHandler.recoverInline(self)
            else:
                self._errHandler.reportMatch(self)
                self.consume()
            self.state = 432
            self.expr()
            self.state = 434
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==94:
                self.state = 433
                self.match(DuanLangParser.PERIOD)


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

        def primary(self):
            return self.getTypedRuleContext(DuanLangParser.PrimaryContext,0)


        def DOT(self):
            return self.getToken(DuanLangParser.DOT, 0)

        def getRuleIndex(self):
            return DuanLangParser.RULE_target

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterTarget" ):
                listener.enterTarget(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitTarget" ):
                listener.exitTarget(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitTarget" ):
                return visitor.visitTarget(self)
            else:
                return visitor.visitChildren(self)




    def target(self):

        localctx = DuanLangParser.TargetContext(self, self._ctx, self.state)
        self.enterRule(localctx, 52, self.RULE_target)
        try:
            self.state = 445
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,54,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 436
                self.match(DuanLangParser.ID)
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 437
                self.expr()
                self.state = 438
                self.match(DuanLangParser.K_OF)
                self.state = 439
                self.match(DuanLangParser.ID)
                pass

            elif la_ == 3:
                self.enterOuterAlt(localctx, 3)
                self.state = 441
                self.primary()
                self.state = 442
                self.match(DuanLangParser.DOT)
                self.state = 443
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


        def K_END(self):
            return self.getToken(DuanLangParser.K_END, 0)

        def K_ELSE_IF(self, i:int=None):
            if i is None:
                return self.getTokens(DuanLangParser.K_ELSE_IF)
            else:
                return self.getToken(DuanLangParser.K_ELSE_IF, i)

        def K_ELSE(self):
            return self.getToken(DuanLangParser.K_ELSE, 0)

        def PERIOD(self):
            return self.getToken(DuanLangParser.PERIOD, 0)

        def getRuleIndex(self):
            return DuanLangParser.RULE_ifStmt

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterIfStmt" ):
                listener.enterIfStmt(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitIfStmt" ):
                listener.exitIfStmt(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitIfStmt" ):
                return visitor.visitIfStmt(self)
            else:
                return visitor.visitChildren(self)




    def ifStmt(self):

        localctx = DuanLangParser.IfStmtContext(self, self._ctx, self.state)
        self.enterRule(localctx, 54, self.RULE_ifStmt)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 447
            self.match(DuanLangParser.K_IF)
            self.state = 448
            self.expr()
            self.state = 449
            self.match(DuanLangParser.COLON)
            self.state = 450
            self.block()
            self.state = 458
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==5:
                self.state = 451
                self.match(DuanLangParser.K_ELSE_IF)
                self.state = 452
                self.expr()
                self.state = 453
                self.match(DuanLangParser.COLON)
                self.state = 454
                self.block()
                self.state = 460
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 464
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==8:
                self.state = 461
                self.match(DuanLangParser.K_ELSE)
                self.state = 462
                self.match(DuanLangParser.COLON)
                self.state = 463
                self.block()


            self.state = 466
            self.match(DuanLangParser.K_END)
            self.state = 468
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==94:
                self.state = 467
                self.match(DuanLangParser.PERIOD)


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

        def ID(self):
            return self.getToken(DuanLangParser.ID, 0)

        def expr(self):
            return self.getTypedRuleContext(DuanLangParser.ExprContext,0)


        def COLON(self):
            return self.getToken(DuanLangParser.COLON, 0)

        def block(self):
            return self.getTypedRuleContext(DuanLangParser.BlockContext,0)


        def K_END(self):
            return self.getToken(DuanLangParser.K_END, 0)

        def K_OF(self):
            return self.getToken(DuanLangParser.K_OF, 0)

        def K_AT(self):
            return self.getToken(DuanLangParser.K_AT, 0)

        def PERIOD(self):
            return self.getToken(DuanLangParser.PERIOD, 0)

        def getRuleIndex(self):
            return DuanLangParser.RULE_foreachStmt

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterForeachStmt" ):
                listener.enterForeachStmt(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitForeachStmt" ):
                listener.exitForeachStmt(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitForeachStmt" ):
                return visitor.visitForeachStmt(self)
            else:
                return visitor.visitChildren(self)




    def foreachStmt(self):

        localctx = DuanLangParser.ForeachStmtContext(self, self._ctx, self.state)
        self.enterRule(localctx, 56, self.RULE_foreachStmt)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 470
            self.match(DuanLangParser.K_FOREACH)
            self.state = 471
            self.match(DuanLangParser.ID)
            self.state = 472
            _la = self._input.LA(1)
            if not(_la==60 or _la==61):
                self._errHandler.recoverInline(self)
            else:
                self._errHandler.reportMatch(self)
                self.consume()
            self.state = 473
            self.expr()
            self.state = 474
            self.match(DuanLangParser.COLON)
            self.state = 475
            self.block()
            self.state = 476
            self.match(DuanLangParser.K_END)
            self.state = 478
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==94:
                self.state = 477
                self.match(DuanLangParser.PERIOD)


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

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterForeachVar" ):
                listener.enterForeachVar(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitForeachVar" ):
                listener.exitForeachVar(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitForeachVar" ):
                return visitor.visitForeachVar(self)
            else:
                return visitor.visitChildren(self)




    def foreachVar(self):

        localctx = DuanLangParser.ForeachVarContext(self, self._ctx, self.state)
        self.enterRule(localctx, 58, self.RULE_foreachVar)
        try:
            self.state = 489
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,59,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 480
                self.match(DuanLangParser.ID)
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 481
                self.match(DuanLangParser.ID)
                self.state = 482
                self.match(DuanLangParser.K_OF)
                self.state = 483
                self.match(DuanLangParser.ID)
                pass

            elif la_ == 3:
                self.enterOuterAlt(localctx, 3)
                self.state = 484
                self.match(DuanLangParser.ID)
                self.state = 485
                self.match(DuanLangParser.K_OF)
                self.state = 486
                self.match(DuanLangParser.ID)
                self.state = 487
                self.match(DuanLangParser.COMMA)
                self.state = 488
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


        def PERIOD(self):
            return self.getToken(DuanLangParser.PERIOD, 0)

        def getRuleIndex(self):
            return DuanLangParser.RULE_whileStmt

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterWhileStmt" ):
                listener.enterWhileStmt(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitWhileStmt" ):
                listener.exitWhileStmt(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitWhileStmt" ):
                return visitor.visitWhileStmt(self)
            else:
                return visitor.visitChildren(self)




    def whileStmt(self):

        localctx = DuanLangParser.WhileStmtContext(self, self._ctx, self.state)
        self.enterRule(localctx, 60, self.RULE_whileStmt)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 491
            self.match(DuanLangParser.K_WHILE)
            self.state = 492
            self.expr()
            self.state = 495
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==96:
                self.state = 493
                self.match(DuanLangParser.COLON)
                self.state = 494
                self.block()


            self.state = 497
            self.match(DuanLangParser.K_END)
            self.state = 499
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==94:
                self.state = 498
                self.match(DuanLangParser.PERIOD)


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


        def PERIOD(self):
            return self.getToken(DuanLangParser.PERIOD, 0)

        def getRuleIndex(self):
            return DuanLangParser.RULE_returnStmt

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterReturnStmt" ):
                listener.enterReturnStmt(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitReturnStmt" ):
                listener.exitReturnStmt(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitReturnStmt" ):
                return visitor.visitReturnStmt(self)
            else:
                return visitor.visitChildren(self)




    def returnStmt(self):

        localctx = DuanLangParser.ReturnStmtContext(self, self._ctx, self.state)
        self.enterRule(localctx, 62, self.RULE_returnStmt)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 501
            self.match(DuanLangParser.K_RETURN)
            self.state = 503
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,62,self._ctx)
            if la_ == 1:
                self.state = 502
                self.expr()


            self.state = 506
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==94:
                self.state = 505
                self.match(DuanLangParser.PERIOD)


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

        def PERIOD(self):
            return self.getToken(DuanLangParser.PERIOD, 0)

        def getRuleIndex(self):
            return DuanLangParser.RULE_breakStmt

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterBreakStmt" ):
                listener.enterBreakStmt(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitBreakStmt" ):
                listener.exitBreakStmt(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitBreakStmt" ):
                return visitor.visitBreakStmt(self)
            else:
                return visitor.visitChildren(self)




    def breakStmt(self):

        localctx = DuanLangParser.BreakStmtContext(self, self._ctx, self.state)
        self.enterRule(localctx, 64, self.RULE_breakStmt)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 508
            self.match(DuanLangParser.K_BREAK)
            self.state = 510
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==94:
                self.state = 509
                self.match(DuanLangParser.PERIOD)


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

        def PERIOD(self):
            return self.getToken(DuanLangParser.PERIOD, 0)

        def getRuleIndex(self):
            return DuanLangParser.RULE_continueStmt

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterContinueStmt" ):
                listener.enterContinueStmt(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitContinueStmt" ):
                listener.exitContinueStmt(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitContinueStmt" ):
                return visitor.visitContinueStmt(self)
            else:
                return visitor.visitChildren(self)




    def continueStmt(self):

        localctx = DuanLangParser.ContinueStmtContext(self, self._ctx, self.state)
        self.enterRule(localctx, 66, self.RULE_continueStmt)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 512
            self.match(DuanLangParser.K_CONTINUE)
            self.state = 514
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==94:
                self.state = 513
                self.match(DuanLangParser.PERIOD)


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

        def PERIOD(self):
            return self.getToken(DuanLangParser.PERIOD, 0)

        def getRuleIndex(self):
            return DuanLangParser.RULE_tryStmt

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterTryStmt" ):
                listener.enterTryStmt(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitTryStmt" ):
                listener.exitTryStmt(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitTryStmt" ):
                return visitor.visitTryStmt(self)
            else:
                return visitor.visitChildren(self)




    def tryStmt(self):

        localctx = DuanLangParser.TryStmtContext(self, self._ctx, self.state)
        self.enterRule(localctx, 68, self.RULE_tryStmt)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 516
            self.match(DuanLangParser.K_TRY)
            self.state = 517
            self.match(DuanLangParser.COLON)
            self.state = 518
            self.block()
            self.state = 519
            self.match(DuanLangParser.K_CATCH)
            self.state = 520
            self.match(DuanLangParser.ID)
            self.state = 521
            self.match(DuanLangParser.COLON)
            self.state = 522
            self.block()
            self.state = 523
            self.match(DuanLangParser.K_END)
            self.state = 525
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==94:
                self.state = 524
                self.match(DuanLangParser.PERIOD)


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


        def PERIOD(self):
            return self.getToken(DuanLangParser.PERIOD, 0)

        def getRuleIndex(self):
            return DuanLangParser.RULE_throwStmt

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterThrowStmt" ):
                listener.enterThrowStmt(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitThrowStmt" ):
                listener.exitThrowStmt(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitThrowStmt" ):
                return visitor.visitThrowStmt(self)
            else:
                return visitor.visitChildren(self)




    def throwStmt(self):

        localctx = DuanLangParser.ThrowStmtContext(self, self._ctx, self.state)
        self.enterRule(localctx, 70, self.RULE_throwStmt)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 527
            self.match(DuanLangParser.K_THROW)
            self.state = 528
            self.expr()
            self.state = 530
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==94:
                self.state = 529
                self.match(DuanLangParser.PERIOD)


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

        def PERIOD(self):
            return self.getToken(DuanLangParser.PERIOD, 0)

        def getRuleIndex(self):
            return DuanLangParser.RULE_printStmt

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterPrintStmt" ):
                listener.enterPrintStmt(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitPrintStmt" ):
                listener.exitPrintStmt(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitPrintStmt" ):
                return visitor.visitPrintStmt(self)
            else:
                return visitor.visitChildren(self)




    def printStmt(self):

        localctx = DuanLangParser.PrintStmtContext(self, self._ctx, self.state)
        self.enterRule(localctx, 72, self.RULE_printStmt)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 532
            _la = self._input.LA(1)
            if not(_la==36 or _la==37):
                self._errHandler.recoverInline(self)
            else:
                self._errHandler.reportMatch(self)
                self.consume()
            self.state = 533
            self.expr()
            self.state = 535
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==94:
                self.state = 534
                self.match(DuanLangParser.PERIOD)


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


        def PERIOD(self):
            return self.getToken(DuanLangParser.PERIOD, 0)

        def getRuleIndex(self):
            return DuanLangParser.RULE_exprStmt

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterExprStmt" ):
                listener.enterExprStmt(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitExprStmt" ):
                listener.exitExprStmt(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitExprStmt" ):
                return visitor.visitExprStmt(self)
            else:
                return visitor.visitChildren(self)




    def exprStmt(self):

        localctx = DuanLangParser.ExprStmtContext(self, self._ctx, self.state)
        self.enterRule(localctx, 74, self.RULE_exprStmt)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 537
            self.expr()
            self.state = 538
            self.match(DuanLangParser.PERIOD)
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

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterExpr" ):
                listener.enterExpr(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitExpr" ):
                listener.exitExpr(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitExpr" ):
                return visitor.visitExpr(self)
            else:
                return visitor.visitChildren(self)




    def expr(self):

        localctx = DuanLangParser.ExprContext(self, self._ctx, self.state)
        self.enterRule(localctx, 76, self.RULE_expr)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 540
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

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterPipelineExpr" ):
                listener.enterPipelineExpr(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitPipelineExpr" ):
                listener.exitPipelineExpr(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitPipelineExpr" ):
                return visitor.visitPipelineExpr(self)
            else:
                return visitor.visitChildren(self)




    def pipelineExpr(self):

        localctx = DuanLangParser.PipelineExprContext(self, self._ctx, self.state)
        self.enterRule(localctx, 78, self.RULE_pipelineExpr)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 542
            self.andExpr()
            self.state = 547
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==59 or _la==91:
                self.state = 543
                _la = self._input.LA(1)
                if not(_la==59 or _la==91):
                    self._errHandler.recoverInline(self)
                else:
                    self._errHandler.reportMatch(self)
                    self.consume()
                self.state = 544
                self.andExpr()
                self.state = 549
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

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterAndExpr" ):
                listener.enterAndExpr(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitAndExpr" ):
                listener.exitAndExpr(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitAndExpr" ):
                return visitor.visitAndExpr(self)
            else:
                return visitor.visitChildren(self)




    def andExpr(self):

        localctx = DuanLangParser.AndExprContext(self, self._ctx, self.state)
        self.enterRule(localctx, 80, self.RULE_andExpr)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 550
            self.orExpr()
            self.state = 555
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==50:
                self.state = 551
                self.match(DuanLangParser.K_AND)
                self.state = 552
                self.orExpr()
                self.state = 557
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

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterOrExpr" ):
                listener.enterOrExpr(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitOrExpr" ):
                listener.exitOrExpr(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitOrExpr" ):
                return visitor.visitOrExpr(self)
            else:
                return visitor.visitChildren(self)




    def orExpr(self):

        localctx = DuanLangParser.OrExprContext(self, self._ctx, self.state)
        self.enterRule(localctx, 82, self.RULE_orExpr)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 558
            self.comparisonExpr()
            self.state = 563
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==51:
                self.state = 559
                self.match(DuanLangParser.K_OR)
                self.state = 560
                self.comparisonExpr()
                self.state = 565
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

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterComparisonExpr" ):
                listener.enterComparisonExpr(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitComparisonExpr" ):
                listener.exitComparisonExpr(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitComparisonExpr" ):
                return visitor.visitComparisonExpr(self)
            else:
                return visitor.visitChildren(self)




    def comparisonExpr(self):

        localctx = DuanLangParser.ComparisonExprContext(self, self._ctx, self.state)
        self.enterRule(localctx, 84, self.RULE_comparisonExpr)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 566
            self.additiveExpr()
            self.state = 572
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while (((_la) & ~0x3f) == 0 and ((1 << _la) & 293888) != 0) or ((((_la - 81)) & ~0x3f) == 0 and ((1 << (_la - 81)) & 63) != 0):
                self.state = 567
                self.compOp()
                self.state = 568
                self.additiveExpr()
                self.state = 574
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

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterCompOp" ):
                listener.enterCompOp(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitCompOp" ):
                listener.exitCompOp(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitCompOp" ):
                return visitor.visitCompOp(self)
            else:
                return visitor.visitChildren(self)




    def compOp(self):

        localctx = DuanLangParser.CompOpContext(self, self._ctx, self.state)
        self.enterRule(localctx, 86, self.RULE_compOp)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 575
            _la = self._input.LA(1)
            if not((((_la) & ~0x3f) == 0 and ((1 << _la) & 293888) != 0) or ((((_la - 81)) & ~0x3f) == 0 and ((1 << (_la - 81)) & 63) != 0)):
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

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterAdditiveExpr" ):
                listener.enterAdditiveExpr(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitAdditiveExpr" ):
                listener.exitAdditiveExpr(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitAdditiveExpr" ):
                return visitor.visitAdditiveExpr(self)
            else:
                return visitor.visitChildren(self)




    def additiveExpr(self):

        localctx = DuanLangParser.AdditiveExprContext(self, self._ctx, self.state)
        self.enterRule(localctx, 88, self.RULE_additiveExpr)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 577
            self.multiplicativeExpr()
            self.state = 583
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,73,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    self.state = 578
                    self.addOp()
                    self.state = 579
                    self.multiplicativeExpr() 
                self.state = 585
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,73,self._ctx)

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

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterAddOp" ):
                listener.enterAddOp(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitAddOp" ):
                listener.exitAddOp(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitAddOp" ):
                return visitor.visitAddOp(self)
            else:
                return visitor.visitChildren(self)




    def addOp(self):

        localctx = DuanLangParser.AddOpContext(self, self._ctx, self.state)
        self.enterRule(localctx, 90, self.RULE_addOp)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 586
            _la = self._input.LA(1)
            if not(((((_la - 53)) & ~0x3f) == 0 and ((1 << (_la - 53)) & 201326595) != 0)):
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

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterMultiplicativeExpr" ):
                listener.enterMultiplicativeExpr(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitMultiplicativeExpr" ):
                listener.exitMultiplicativeExpr(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitMultiplicativeExpr" ):
                return visitor.visitMultiplicativeExpr(self)
            else:
                return visitor.visitChildren(self)




    def multiplicativeExpr(self):

        localctx = DuanLangParser.MultiplicativeExprContext(self, self._ctx, self.state)
        self.enterRule(localctx, 92, self.RULE_multiplicativeExpr)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 588
            self.unaryExpr()
            self.state = 594
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while ((((_la - 55)) & ~0x3f) == 0 and ((1 << (_la - 55)) & 15728655) != 0):
                self.state = 589
                self.multOp()
                self.state = 590
                self.unaryExpr()
                self.state = 596
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

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterMultOp" ):
                listener.enterMultOp(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitMultOp" ):
                listener.exitMultOp(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitMultOp" ):
                return visitor.visitMultOp(self)
            else:
                return visitor.visitChildren(self)




    def multOp(self):

        localctx = DuanLangParser.MultOpContext(self, self._ctx, self.state)
        self.enterRule(localctx, 94, self.RULE_multOp)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 597
            _la = self._input.LA(1)
            if not(((((_la - 55)) & ~0x3f) == 0 and ((1 << (_la - 55)) & 15728655) != 0)):
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

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterUnaryExpr" ):
                listener.enterUnaryExpr(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitUnaryExpr" ):
                listener.exitUnaryExpr(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitUnaryExpr" ):
                return visitor.visitUnaryExpr(self)
            else:
                return visitor.visitChildren(self)




    def unaryExpr(self):

        localctx = DuanLangParser.UnaryExprContext(self, self._ctx, self.state)
        self.enterRule(localctx, 96, self.RULE_unaryExpr)
        self._la = 0 # Token type
        try:
            self.state = 604
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [52, 88]:
                self.enterOuterAlt(localctx, 1)
                self.state = 599
                _la = self._input.LA(1)
                if not(_la==52 or _la==88):
                    self._errHandler.recoverInline(self)
                else:
                    self._errHandler.reportMatch(self)
                    self.consume()
                self.state = 600
                self.unaryExpr()
                pass
            elif token in [54, 80]:
                self.enterOuterAlt(localctx, 2)
                self.state = 601
                _la = self._input.LA(1)
                if not(_la==54 or _la==80):
                    self._errHandler.recoverInline(self)
                else:
                    self._errHandler.reportMatch(self)
                    self.consume()
                self.state = 602
                self.unaryExpr()
                pass
            elif token in [45, 49, 63, 64, 65, 99, 101, 105, 107, 108, 109]:
                self.enterOuterAlt(localctx, 3)
                self.state = 603
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

        def DOT(self, i:int=None):
            if i is None:
                return self.getTokens(DuanLangParser.DOT)
            else:
                return self.getToken(DuanLangParser.DOT, i)

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

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterPostfixExpr" ):
                listener.enterPostfixExpr(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitPostfixExpr" ):
                listener.exitPostfixExpr(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitPostfixExpr" ):
                return visitor.visitPostfixExpr(self)
            else:
                return visitor.visitChildren(self)




    def postfixExpr(self):

        localctx = DuanLangParser.PostfixExprContext(self, self._ctx, self.state)
        self.enterRule(localctx, 98, self.RULE_postfixExpr)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 606
            self.primary()
            self.state = 630
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,79,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    self.state = 628
                    self._errHandler.sync(self)
                    token = self._input.LA(1)
                    if token in [105]:
                        self.state = 607
                        self.match(DuanLangParser.BOOK_L)
                        self.state = 608
                        self.match(DuanLangParser.ID)
                        self.state = 609
                        self.match(DuanLangParser.BOOK_R)
                        self.state = 610
                        self.match(DuanLangParser.LPAREN)
                        self.state = 612
                        self._errHandler.sync(self)
                        _la = self._input.LA(1)
                        if (((_la) & ~0x3f) == 0 and ((1 << _la) & -9200255904392413184) != 0) or ((((_la - 64)) & ~0x3f) == 0 and ((1 << (_la - 64)) & 63943489945603) != 0):
                            self.state = 611
                            self.exprList()


                        self.state = 614
                        self.match(DuanLangParser.RPAREN)
                        pass
                    elif token in [99]:
                        self.state = 615
                        self.match(DuanLangParser.LPAREN)
                        self.state = 617
                        self._errHandler.sync(self)
                        _la = self._input.LA(1)
                        if (((_la) & ~0x3f) == 0 and ((1 << _la) & -9200255904392413184) != 0) or ((((_la - 64)) & ~0x3f) == 0 and ((1 << (_la - 64)) & 63943489945603) != 0):
                            self.state = 616
                            self.exprList()


                        self.state = 619
                        self.match(DuanLangParser.RPAREN)
                        pass
                    elif token in [93]:
                        self.state = 620
                        self.match(DuanLangParser.DOT)
                        self.state = 621
                        self.match(DuanLangParser.ID)
                        pass
                    elif token in [60]:
                        self.state = 622
                        self.match(DuanLangParser.K_OF)
                        self.state = 623
                        self.match(DuanLangParser.ID)
                        pass
                    elif token in [101]:
                        self.state = 624
                        self.match(DuanLangParser.LBRACKET)
                        self.state = 625
                        self.expr()
                        self.state = 626
                        self.match(DuanLangParser.RBRACKET)
                        pass
                    else:
                        raise NoViableAltException(self)
             
                self.state = 632
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,79,self._ctx)

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

        def K_SELF(self):
            return self.getToken(DuanLangParser.K_SELF, 0)

        def K_NEW(self):
            return self.getToken(DuanLangParser.K_NEW, 0)

        def ID(self):
            return self.getToken(DuanLangParser.ID, 0)

        def LPAREN(self):
            return self.getToken(DuanLangParser.LPAREN, 0)

        def RPAREN(self):
            return self.getToken(DuanLangParser.RPAREN, 0)

        def exprList(self):
            return self.getTypedRuleContext(DuanLangParser.ExprListContext,0)


        def expr(self):
            return self.getTypedRuleContext(DuanLangParser.ExprContext,0)


        def LBRACKET(self):
            return self.getToken(DuanLangParser.LBRACKET, 0)

        def dictLiteral(self):
            return self.getTypedRuleContext(DuanLangParser.DictLiteralContext,0)


        def RBRACKET(self):
            return self.getToken(DuanLangParser.RBRACKET, 0)

        def BOOK_L(self):
            return self.getToken(DuanLangParser.BOOK_L, 0)

        def BOOK_R(self):
            return self.getToken(DuanLangParser.BOOK_R, 0)

        def getRuleIndex(self):
            return DuanLangParser.RULE_primary

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterPrimary" ):
                listener.enterPrimary(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitPrimary" ):
                listener.exitPrimary(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitPrimary" ):
                return visitor.visitPrimary(self)
            else:
                return visitor.visitChildren(self)




    def primary(self):

        localctx = DuanLangParser.PrimaryContext(self, self._ctx, self.state)
        self.enterRule(localctx, 100, self.RULE_primary)
        self._la = 0 # Token type
        try:
            self.state = 663
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,82,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 633
                self.match(DuanLangParser.NUMBER)
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 634
                self.match(DuanLangParser.STRING)
                pass

            elif la_ == 3:
                self.enterOuterAlt(localctx, 3)
                self.state = 635
                self.match(DuanLangParser.K_TRUE)
                pass

            elif la_ == 4:
                self.enterOuterAlt(localctx, 4)
                self.state = 636
                self.match(DuanLangParser.K_FALSE)
                pass

            elif la_ == 5:
                self.enterOuterAlt(localctx, 5)
                self.state = 637
                self.match(DuanLangParser.K_NULL)
                pass

            elif la_ == 6:
                self.enterOuterAlt(localctx, 6)
                self.state = 638
                self.match(DuanLangParser.K_SELF)
                pass

            elif la_ == 7:
                self.enterOuterAlt(localctx, 7)
                self.state = 639
                self.match(DuanLangParser.K_NEW)
                self.state = 640
                self.match(DuanLangParser.ID)
                self.state = 641
                self.match(DuanLangParser.LPAREN)
                self.state = 643
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if (((_la) & ~0x3f) == 0 and ((1 << _la) & -9200255904392413184) != 0) or ((((_la - 64)) & ~0x3f) == 0 and ((1 << (_la - 64)) & 63943489945603) != 0):
                    self.state = 642
                    self.exprList()


                self.state = 645
                self.match(DuanLangParser.RPAREN)
                pass

            elif la_ == 8:
                self.enterOuterAlt(localctx, 8)
                self.state = 646
                self.match(DuanLangParser.ID)
                pass

            elif la_ == 9:
                self.enterOuterAlt(localctx, 9)
                self.state = 647
                self.match(DuanLangParser.LPAREN)
                self.state = 648
                self.expr()
                self.state = 649
                self.match(DuanLangParser.RPAREN)
                pass

            elif la_ == 10:
                self.enterOuterAlt(localctx, 10)
                self.state = 651
                self.match(DuanLangParser.LBRACKET)
                self.state = 652
                self.dictLiteral()
                self.state = 653
                self.match(DuanLangParser.RBRACKET)
                pass

            elif la_ == 11:
                self.enterOuterAlt(localctx, 11)
                self.state = 655
                self.match(DuanLangParser.LBRACKET)
                self.state = 657
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if (((_la) & ~0x3f) == 0 and ((1 << _la) & -9200255904392413184) != 0) or ((((_la - 64)) & ~0x3f) == 0 and ((1 << (_la - 64)) & 63943489945603) != 0):
                    self.state = 656
                    self.exprList()


                self.state = 659
                self.match(DuanLangParser.RBRACKET)
                pass

            elif la_ == 12:
                self.enterOuterAlt(localctx, 12)
                self.state = 660
                self.match(DuanLangParser.BOOK_L)
                self.state = 661
                self.match(DuanLangParser.ID)
                self.state = 662
                self.match(DuanLangParser.BOOK_R)
                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class DictLiteralContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def dictEntry(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(DuanLangParser.DictEntryContext)
            else:
                return self.getTypedRuleContext(DuanLangParser.DictEntryContext,i)


        def COMMA(self, i:int=None):
            if i is None:
                return self.getTokens(DuanLangParser.COMMA)
            else:
                return self.getToken(DuanLangParser.COMMA, i)

        def getRuleIndex(self):
            return DuanLangParser.RULE_dictLiteral

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterDictLiteral" ):
                listener.enterDictLiteral(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitDictLiteral" ):
                listener.exitDictLiteral(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitDictLiteral" ):
                return visitor.visitDictLiteral(self)
            else:
                return visitor.visitChildren(self)




    def dictLiteral(self):

        localctx = DuanLangParser.DictLiteralContext(self, self._ctx, self.state)
        self.enterRule(localctx, 102, self.RULE_dictLiteral)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 665
            self.dictEntry()
            self.state = 670
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==95:
                self.state = 666
                self.match(DuanLangParser.COMMA)
                self.state = 667
                self.dictEntry()
                self.state = 672
                self._errHandler.sync(self)
                _la = self._input.LA(1)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class DictEntryContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def expr(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(DuanLangParser.ExprContext)
            else:
                return self.getTypedRuleContext(DuanLangParser.ExprContext,i)


        def COLON(self):
            return self.getToken(DuanLangParser.COLON, 0)

        def getRuleIndex(self):
            return DuanLangParser.RULE_dictEntry

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterDictEntry" ):
                listener.enterDictEntry(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitDictEntry" ):
                listener.exitDictEntry(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitDictEntry" ):
                return visitor.visitDictEntry(self)
            else:
                return visitor.visitChildren(self)




    def dictEntry(self):

        localctx = DuanLangParser.DictEntryContext(self, self._ctx, self.state)
        self.enterRule(localctx, 104, self.RULE_dictEntry)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 673
            self.expr()
            self.state = 674
            self.match(DuanLangParser.COLON)
            self.state = 675
            self.expr()
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

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterTypeAnnotation" ):
                listener.enterTypeAnnotation(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitTypeAnnotation" ):
                listener.exitTypeAnnotation(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitTypeAnnotation" ):
                return visitor.visitTypeAnnotation(self)
            else:
                return visitor.visitChildren(self)




    def typeAnnotation(self):

        localctx = DuanLangParser.TypeAnnotationContext(self, self._ctx, self.state)
        self.enterRule(localctx, 106, self.RULE_typeAnnotation)
        try:
            self.state = 679
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [65, 66, 67, 68, 69, 70, 71, 72, 73, 74]:
                self.enterOuterAlt(localctx, 1)
                self.state = 677
                self.builtinType()
                pass
            elif token in [109]:
                self.enterOuterAlt(localctx, 2)
                self.state = 678
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

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterBuiltinType" ):
                listener.enterBuiltinType(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitBuiltinType" ):
                listener.exitBuiltinType(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitBuiltinType" ):
                return visitor.visitBuiltinType(self)
            else:
                return visitor.visitChildren(self)




    def builtinType(self):

        localctx = DuanLangParser.BuiltinTypeContext(self, self._ctx, self.state)
        self.enterRule(localctx, 108, self.RULE_builtinType)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 681
            _la = self._input.LA(1)
            if not(((((_la - 65)) & ~0x3f) == 0 and ((1 << (_la - 65)) & 1023) != 0)):
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

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterExprList" ):
                listener.enterExprList(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitExprList" ):
                listener.exitExprList(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitExprList" ):
                return visitor.visitExprList(self)
            else:
                return visitor.visitChildren(self)




    def exprList(self):

        localctx = DuanLangParser.ExprListContext(self, self._ctx, self.state)
        self.enterRule(localctx, 110, self.RULE_exprList)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 683
            self.expr()
            self.state = 688
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==95:
                self.state = 684
                self.match(DuanLangParser.COMMA)
                self.state = 685
                self.expr()
                self.state = 690
                self._errHandler.sync(self)
                _la = self._input.LA(1)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx





