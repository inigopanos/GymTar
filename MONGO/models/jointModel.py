import uuid
from typing import Optional, List, Union
from pydantic import BaseModel, Field

class Keypoint(BaseModel):
    x: Union[float, None]
    y: Union[float, None]
    z: Union[float, None]

class BodyItem(BaseModel):
    id: int
    unique_object_id: str
    tracking_state: str
    action_state: str
    position: List[float]
    confidence: float
    keypoint: List[Keypoint]
    local_position_per_joint: List[float]
    local_orientation_per_joint: List[float]

class JointSchema(BaseModel):
    is_new: bool
    is_tracked: bool
    timestamp: List[int]
    body_list: List[BodyItem]

    class Config:
        orm_mode = True

def replace_nan_with_none(data):
    if isinstance(data, list):
        print('Data is list')
        return [replace_nan_with_none(item) for item in data["keypoint"]]
    elif isinstance(data, dict):
        print('Data is dict')
        return {key: replace_nan_with_none(value) for key, value in data.items()}
    else:
        return data


# Crea una instancia de JointSchema usando paréntesis, no llaves
documento = JointSchema(
    is_new=True,
    is_tracked=False,
    timestamp=[1692783040531070201],
    body_list=[
        {
            "id": 0,
            "unique_object_id": "8a8ef213-860c-4f5a-9260-1cda25286937",
            "tracking_state": "ON",
            "action_state": "Unknown",
            "position": [-0.15865983068943024, 0.6491988897323608, -2.568483829498291],
            "confidence": 96.8031997680664,
            "keypoint": [
                    [
                        0.7719746232032776,
                        0.724526047706604,
                        -2.5380563735961914
                    ],
                    [
                        0.7754035592079163,
                        0.8480128049850464,
                        -2.533350944519043
                    ],
                    [
                        0.7501696944236755,
                        0.984819769859314,
                        -2.4649105072021484
                    ],
                    [
                        0.7583850026130676,
                        1.1040924787521362,
                        -2.4763023853302
                    ],
                    [
                        0.7692028284072876,
                        1.2257440090179443,
                        -2.511645555496216
                    ],
                    [
                        1.019333839416504,
                        1.3761675357818604,
                        -2.691791296005249
                    ],
                    [
                        None,
                        None,
                        None
                    ],
                    [
                        0.9990243911743164,
                        1.4013081789016724,
                        -2.6893563270568848
                    ],
                    [
                        None,
                        None,
                        None
                    ],
                    [
                        0.9098328948020935,
                        1.380531668663025,
                        -2.699871778488159
                    ],
                    [
                        0.785000205039978,
                        1.225883960723877,
                        -2.578881025314331
                    ],
                    [
                        0.7893800139427185,
                        1.2253762483596802,
                        -2.561410665512085
                    ],
                    [
                        0.7851216793060303,
                        1.2258882522583008,
                        -2.5793135166168213
                    ],
                    [
                        0.7803170680999756,
                        1.2279003858566284,
                        -2.536954164505005
                    ],
                    [
                        None,
                        None,
                        None
                    ],
                    [
                        0.7623891830444336,
                        1.0052614212036133,
                        -2.458089590072632
                    ],
                    [
                        None,
                        None,
                        None
                    ],
                    [
                        0.8751031756401062,
                        0.7935078144073486,
                        -2.469264507293701
                    ],
                    [
                        0.7635850310325623,
                        0.7298998832702637,
                        -2.5506248474121094
                    ],
                    [
                        0.7586101293563843,
                        0.7365037798881531,
                        -2.446228265762329
                    ],
                    [
                        0.7952609062194824,
                        0.31272637844085693,
                        -2.6977038383483887
                    ],
                    [
                        0.8087487816810608,
                        0.3319982588291168,
                        -2.4947509765625
                    ],
                    [
                        0.7120130658149719,
                        0.014385033398866653,
                        -2.5921850204467773
                    ],
                    [
                        0.697424054145813,
                        -0.03443057835102081,
                        -2.5489039421081543
                    ],
                    [
                        None,
                        None,
                        None
                    ],
                    [
                        0.826650857925415,
                        -0.13885632157325745,
                        -2.4927024841308594
                    ],
                    [
                        None,
                        None,
                        None
                    ],
                    [
                        0.7455083727836609,
                        -0.13242977857589722,
                        -2.4440767765045166
                    ],
                    [
                        None,
                        None,
                        None
                    ],
                    [
                        0.6658102869987488,
                        -0.10564111918210983,
                        -2.6184937953948975
                    ],
                    [
                        None,
                        None,
                        None
                    ],
                    [
                        0.9132776856422424,
                        0.6688142418861389,
                        -2.4861953258514404
                    ],
                    [
                        None,
                        None,
                        None
                    ],
                    [
                        0.960108757019043,
                        0.6642115116119385,
                        -2.569788932800293
                    ],
                    [
                        None,
                        None,
                        None
                    ],
                    [
                        None,
                        None,
                        None
                    ],
                    [
                        None,
                        None,
                        None
                    ],
                    [
                        None,
                        None,
                        None
                    ]
                ],
            "local_position_per_joint": [],
            "local_orientation_per_joint": []
        }
    ]
)

joint_data = replace_nan_with_none(documento)
print("Joint data en jointModel.py: ", joint_data)