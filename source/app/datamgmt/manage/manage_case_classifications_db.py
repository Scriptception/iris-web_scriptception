#!/usr/bin/env python3
#
#  IRIS Source Code
#  contact@dfir-iris.org
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU Lesser General Public
#  License as published by the Free Software Foundation; either
#  version 3 of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
#  Lesser General Public License for more details.
#
#  You should have received a copy of the GNU Lesser General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
from typing import List

from app.models import CaseClassification


def get_case_classifications_list() -> List[dict]:
    """Get a list of case classifications

    Returns:
        List[dict]: List of case classifications
    """
    case_classifications = CaseClassification.query.with_entities(
        CaseClassification.id,
        CaseClassification.name,
        CaseClassification.name_expanded,
        CaseClassification.description,
        CaseClassification.creation_date
    ).all()

    c_cl = [row._asdict() for row in case_classifications]
    return c_cl


def get_case_classification_by_id(cur_id: int) -> CaseClassification:
    """Get a case classification

    Args:
        cur_id (int): case classification id

    Returns:
        CaseClassification: Case classification
    """
    case_classification = CaseClassification.query.filter_by(id=cur_id).first()
    return case_classification
