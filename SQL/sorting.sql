select
    smp.well_position,
    smp.gender_pass as estimated_gender,
from 
    sample_mapping
    order by REVERSE(well_position) asc;

--- A1 B1 C1 D1 .. H1 A2 B2 C2 D2


select
    smp.well_position,
    smp.gender_pass as estimated_gender,
from 
    sample_mapping
    order by CONCAT(LPAD(RIGHT(smp.well_position,-1),2,'0'),LEFT(smp.well_position,1)) asc;

--- 01A 01B 01C 01D ... 02A 02B 02C ........ 12F 12G 12H