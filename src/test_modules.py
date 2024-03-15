from ReefOps import Site, Survey
from ReefCheck import ReefCheck
import pandas as pd
import numpy as np

# Unit testing
def test_site():
    data = {'site_id': 'C-ADQ23-HI-01',
            'site_name': 'Hook Island ADQ',
            'client': 'Abu Dhabi Developmental Holding Company PJSC',
            'type': 'reef_tiles',
            'area_m2': 40,
            'quantity': 160,
            'deployed_tiles': 160,
            'coral_frag': 250,
            'batch_number': 'xxxx',
            'country': 'United Arab Emirates',
            'city': 'Abu Dhabi',
            'locality_name': 'Hook Island',
            'latitude': 24.360425,
            'longitude': 52.762831,
            'start_date': '06/03/2023',
            'end_date': '11/03/2023',
            'status': 'done',
            'project manager': 'Vriko Yu',
            'destroyed tiles': 0,
            'to be deployed': 0
            }
    expected_df = pd.Series(data, name=0)
    site = Site('C-ADQ23-HI-01', pytest=True)
    df = site.site_df
    pd.testing.assert_series_equal(df, expected_df)


def test_survey_id():
    data = {'geographical_code': 'UAE',
            'client_code': 'ADQ',
            'site_id': 'C-ADQ23-HI-01',
            'survey_id': 'S1',
            'survey_type': 'quarterly',
            'status': 'done',
            'planned_date': '11/06/2023',
            'start_date': '06/05/2023',
            'end_date': '07/05/2023',
            'day_interval': 97,
            'actual_interval': 61,
            'offset': 36.0,
            'agents': 'JD, VY, LZ, MY',
            'transplanting': True,
            'reef_check': True,
            'sfm': True,
            'vid360': True,
            'edna': False,
            'dir': 'link',
            'rc_path': 'link',
            'sfm_path': 'link',
            'vid360_path': 'link',
            'remarks': np.nan
            }
    expected_df = pd.Series(data, name=0)
    site = Site('C-ADQ23-HI-01', pytest=True)
    s1 = Survey(site=site, survey_id='S1', pytest=True)
    df = s1.survey_df
    pd.testing.assert_series_equal(df, expected_df)


def test_survey():
    data = {'survey_id': ['S1', 'S2'],
            'geographical_code': ['UAE', 'UAE'],
            'client_code': ['ADQ', 'ADQ'],
            'site_id': ['C-ADQ23-HI-01', 'C-ADQ23-HI-01'],
            'survey_type': ['quarterly', 'quarterly'],
            'status': ['done', 'done'],
            'planned_date': ['11/06/2023', '11/09/2023'],
            'start_date': ['06/05/2023', '09/08/2023'],
            'end_date': ['07/05/2023', '09/08/2023'],
            'day_interval': [97, 189],
            'actual_interval': [61, 156],
            'offset': [36.0, 33.0],
            'agents': ['JD, VY, LZ, MY', 'VY, LZ, DT, MY'],
            'transplanting': [True, False],
            'reef_check': [True, True],
            'sfm': [True, True],
            'vid360': [True, True],
            'edna': [False, False],
            'dir': ['link', 'link'],
            'rc_path': ['link', 'link'],
            'sfm_path': ['link', 'link'],
            'vid360_path': ['link', 'link'],
            'remarks': [np.nan, np.nan]
            }
    expected_df = pd.DataFrame(data)
    site = Site('C-ADQ23-HI-01', pytest=True)
    surveys = Survey(site=site, pytest=True)
    df = surveys.survey_df
    pd.testing.assert_frame_equal(df, expected_df)


def test_reefcheck_id():
    data = {'survey_id': ['S1', 'S1', 'S1', 'S1', 'S1', 'S1'],
            'treatment': ['hive', 'hive', 'hive', 'control', 'control', 'control'],
            'n': [2.0, 1.0, 2.0, 5.0, 22.0, 10.0],
            'common_name': ['Doublebar cardinalfish', 'Indo-Pacific sergeant', 'Rock crab', 'Indo-Pacific sergeant',
                            'Diadema setosa', 'Purple sea urchin'],
            'species': ['Apogonichthyoides sialis', 'Abudefduf vaigiensis', 'na', 'Neopomacentrus bankieri',
                        'Diadema setosum', 'Heliocidaris crassispina'],
            'origin': ['(Jordan & Thompson, 1914)', '(Quoy & Gaimard, 1825)', 'na', '(Richardson, 1846)',
                       '(Leske, 1778)', '(A. Agassiz, 1864)'],
            'family': ['Apogonidae', 'Pomacentridae', 'na', 'Neopomacentrus', 'Diadematidae', 'Echinometridae'],
            'category': ['Fish', 'Fish', 'Invert', 'Fish', 'Invert', 'Invert'],
            'mean_length': [np.nan, np.nan, np.nan, np.nan, np.nan, np.nan],
            'max_length': [np.nan, np.nan, np.nan, np.nan, np.nan, np.nan],
            'min_length': [np.nan, np.nan, np.nan, np.nan, np.nan, np.nan],
            'site_id': ['C-SNG23-MI-01', 'C-SNG23-MI-01', 'C-SNG23-MI-01', 'C-SNG23-MI-01', 'C-SNG23-MI-01',
                        'C-SNG23-MI-01'],
            'indicator': [np.nan, np.nan, np.nan, np.nan, np.nan, np.nan]
            }
    expected_df = pd.DataFrame(data)
    reefcheck_s1 = ReefCheck(site_id='C-SNG23-MI-01', survey_id='S1', pytest=True)
    df = reefcheck_s1.reefcheck_df
    pd.testing.assert_frame_equal(df, expected_df, check_dtype=False)


def test_reefcheck():
    data = {'survey_id': ['S1', 'S1', 'S1', 'S1', 'S1', 'S1', 'S2', 'S2'],
            'treatment': ['hive', 'hive', 'hive', 'control', 'control', 'control', 'hive', 'control'],
            'n': [2.0, 1.0, 2.0, 5.0, 22.0, 10.0, 95.0, 10.0],
            'common_name': ['Doublebar cardinalfish', 'Indo-Pacific sergeant', 'Rock crab', 'Indo-Pacific sergeant',
                            'Diadema setosa', 'Purple sea urchin', 'Diadema setosum', 'Diadema setosum'],
            'species': ['Apogonichthyoides sialis', 'Abudefduf vaigiensis', 'na', 'Neopomacentrus bankieri',
                        'Diadema setosum', 'Heliocidaris crassispina', 'Diadema setosum', 'Diadema setosum'],
            'origin': ['(Jordan & Thompson, 1914)', '(Quoy & Gaimard, 1825)', 'na', '(Richardson, 1846)',
                       '(Leske, 1778)', '(A. Agassiz, 1864)', '(Leske, 1778)', '(Leske, 1778)'],
            'family': ['Apogonidae', 'Pomacentridae', 'na', 'Neopomacentrus', 'Diadematidae', 'Echinometridae',
                       'Diadematidae', 'Diadematidae'],
            'category': ['Fish', 'Fish', 'Invert', 'Fish', 'Invert', 'Invert', 'Invert', 'Invert'],
            'mean_length': [np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan],
            'max_length': [np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan],
            'min_length': [np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan],
            'site_id': ['C-SNG23-MI-01', 'C-SNG23-MI-01', 'C-SNG23-MI-01', 'C-SNG23-MI-01', 'C-SNG23-MI-01',
                        'C-SNG23-MI-01', 'C-SNG23-MI-01', 'C-SNG23-MI-01'],
            'indicator': [np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, 'Y', 'Y']
            }
    expected_df = pd.DataFrame(data)
    reefchecks = ReefCheck(site_id='C-SNG23-MI-01', pytest=True)
    df = reefchecks.reefcheck_df
    pd.testing.assert_frame_equal(df, expected_df)

