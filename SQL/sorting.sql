select
    smp.well_position,
    smp.gender_pass as estimated_gender,
from 
    sample_mapping
    order by REVERSE(well_position) asc;

--- A1 B1 C1 D1 .. H1 A2 B2 C2 D2