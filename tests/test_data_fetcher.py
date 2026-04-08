"""Tests for data_fetcher.py — no network calls required."""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from lib.data_fetcher import (
    SAARC_COUNTRIES,
    CACHE_DIR,
    BASE_URL,
    _read_cache,
    _write_cache,
    extract_study_metrics,
)


# ═══════════════════════════════════════════════════════════
#  SAMPLE STUDY RECORD (mimics CT.gov API v2 response shape)
# ═══════════════════════════════════════════════════════════

SAMPLE_STUDY = {
    "protocolSection": {
        "identificationModule": {
            "nctId": "NCT00000001",
            "briefTitle": "Sample Cardiovascular Trial in India",
        },
        "statusModule": {
            "overallStatus": "COMPLETED",
            "startDateStruct": {"date": "2020-01-15"},
        },
        "designModule": {
            "phases": ["PHASE3"],
            "enrollmentInfo": {"count": 500, "type": "ACTUAL"},
            "designInfo": {"allocation": "RANDOMIZED"},
        },
        "conditionsModule": {
            "conditions": ["Heart Failure", "Cardiomyopathy"],
        },
        "contactsLocationsModule": {
            "locations": [
                {"facility": "AIIMS", "city": "New Delhi", "country": "India"},
                {"facility": "AKU", "city": "Karachi", "country": "Pakistan"},
            ],
        },
        "sponsorCollaboratorsModule": {
            "leadSponsor": {
                "name": "All India Institute of Medical Sciences",
                "class": "OTHER",
            },
        },
    },
}


class TestExtractStudyMetricsEmpty:
    """test_extract_study_metrics_empty: empty list returns zeroed structure."""

    def test_empty_returns_zero_total(self):
        m = extract_study_metrics([])
        assert m["total"] == 0

    def test_empty_statuses(self):
        m = extract_study_metrics([])
        assert m["statuses"] == {}

    def test_empty_phases(self):
        m = extract_study_metrics([])
        assert m["phases"] == {}

    def test_empty_enrollment_values(self):
        m = extract_study_metrics([])
        assert m["enrollment_values"] == []

    def test_empty_start_years(self):
        m = extract_study_metrics([])
        assert m["start_years"] == []

    def test_empty_countries(self):
        m = extract_study_metrics([])
        assert m["countries"] == {}

    def test_empty_cities(self):
        m = extract_study_metrics([])
        assert m["cities"] == {}

    def test_empty_designs(self):
        m = extract_study_metrics([])
        assert m["designs"] == {"randomized": 0, "non_randomized": 0, "observational": 0}

    def test_empty_conditions(self):
        m = extract_study_metrics([])
        assert m["conditions_list"] == []

    def test_empty_sponsors(self):
        m = extract_study_metrics([])
        assert m["sponsors"] == {}

    def test_empty_sponsor_classes(self):
        m = extract_study_metrics([])
        assert m["sponsor_classes"] == {}


class TestExtractStudyMetricsBasic:
    """test_extract_study_metrics_basic: single sample record parsed correctly."""

    def test_total_is_one(self):
        m = extract_study_metrics([SAMPLE_STUDY])
        assert m["total"] == 1

    def test_status_completed(self):
        m = extract_study_metrics([SAMPLE_STUDY])
        assert m["statuses"]["COMPLETED"] == 1

    def test_phase3(self):
        m = extract_study_metrics([SAMPLE_STUDY])
        assert m["phases"]["PHASE3"] == 1

    def test_enrollment(self):
        m = extract_study_metrics([SAMPLE_STUDY])
        assert m["enrollment_values"] == [500]

    def test_start_year(self):
        m = extract_study_metrics([SAMPLE_STUDY])
        assert m["start_years"] == [2020]

    def test_countries(self):
        m = extract_study_metrics([SAMPLE_STUDY])
        assert m["countries"]["India"] == 1
        assert m["countries"]["Pakistan"] == 1

    def test_cities(self):
        m = extract_study_metrics([SAMPLE_STUDY])
        assert m["cities"]["New Delhi"] == 1
        assert m["cities"]["Karachi"] == 1

    def test_design_randomized(self):
        m = extract_study_metrics([SAMPLE_STUDY])
        assert m["designs"]["randomized"] == 1
        assert m["designs"]["non_randomized"] == 0

    def test_conditions(self):
        m = extract_study_metrics([SAMPLE_STUDY])
        assert "Heart Failure" in m["conditions_list"]
        assert "Cardiomyopathy" in m["conditions_list"]

    def test_sponsor_name(self):
        m = extract_study_metrics([SAMPLE_STUDY])
        assert "All India Institute of Medical Sciences" in m["sponsors"]

    def test_sponsor_class(self):
        m = extract_study_metrics([SAMPLE_STUDY])
        assert m["sponsor_classes"]["OTHER"] == 1


class TestCacheWriteAndRead:
    """test_cache_write_and_read: roundtrip through tmp_path."""

    def test_roundtrip(self, tmp_path):
        data = {"slug": "test-slug", "saarc_total": 42, "nested": {"key": "value"}}
        _write_cache("test-slug", data, cache_dir=tmp_path)
        result = _read_cache("test-slug", cache_dir=tmp_path)
        assert result is not None
        assert result["slug"] == "test-slug"
        assert result["saarc_total"] == 42
        assert result["nested"]["key"] == "value"

    def test_overwrite(self, tmp_path):
        _write_cache("overwrite-test", {"version": 1}, cache_dir=tmp_path)
        _write_cache("overwrite-test", {"version": 2}, cache_dir=tmp_path)
        result = _read_cache("overwrite-test", cache_dir=tmp_path)
        assert result["version"] == 2


class TestCacheMissReturnsNone:
    """test_cache_miss_returns_none: nonexistent slug returns None."""

    def test_miss(self, tmp_path):
        result = _read_cache("nonexistent-slug", cache_dir=tmp_path)
        assert result is None

    def test_miss_default_dir(self, tmp_path):
        """Even with a valid directory, a missing slug returns None."""
        result = _read_cache("this-does-not-exist-12345", cache_dir=tmp_path)
        assert result is None


class TestSaarcCountriesInFetcher:
    """test_saarc_countries_in_fetcher: constant matches expected set."""

    def test_count(self):
        assert len(SAARC_COUNTRIES) == 8

    def test_expected_members(self):
        expected = {"India", "Pakistan", "Bangladesh", "Sri Lanka",
                    "Nepal", "Afghanistan", "Bhutan", "Maldives"}
        assert set(SAARC_COUNTRIES) == expected

    def test_base_url(self):
        assert BASE_URL == "https://clinicaltrials.gov/api/v2"

    def test_cache_dir_name(self):
        assert CACHE_DIR.name == "data_cache"
