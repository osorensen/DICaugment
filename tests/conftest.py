import multiprocessing
import sys
import warnings

import numpy as np
import pytest

try:
    import torch  # skipcq: PYL-W0611
    import torchvision  # skipcq: PYL-W0611

    torch_available = True
except ImportError:
    torch_available = False


# try:
#     import imgaug

#     imgaug_available = True
# except ImportError:
#     imgaug_available = False


# skipif_imgaug = pytest.mark.skipif(imgaug_available, reason="The test was skipped because imgaug is installed")
# skipif_no_imgaug = pytest.mark.skipif(
#     not imgaug_available, reason="The test was skipped because imgaug is not installed"
# )
skipif_no_torch = pytest.mark.skipif(
    not torch_available,
    reason="The test was skipped because PyTorch and torchvision are not installed",
)


# def pytest_collection_modifyitems(items):
#     for item in items:
#         if item.get_marker('timeout') is None:
#             item.add_marker(pytest.mark.timeout(3))


def pytest_ignore_collect(path):
    if not torch_available and path.fnmatch("test_pytorch.py"):
        warnings.warn(
            UserWarning(
                "Tests that require PyTorch and torchvision were skipped because those libraries are not installed."
            )
        )
        return True

    # if not imgaug_available and path.fnmatch("test_imgaug.py"):
    #     warnings.warn(UserWarning("Tests that require imgaug were skipped because this library is not installed."))
    #     return True

    return False


@pytest.fixture
def image():
    return np.random.randint(low=0, high=256, size=(100, 100, 100), dtype=np.uint8)


@pytest.fixture
def mask():
    return np.random.randint(low=0, high=2, size=(100, 100, 100), dtype=np.uint8)


@pytest.fixture
def bboxes():
    return [[15, 12, 10, 75, 30, 20, 1], [55, 25, 25, 90, 90, 40, 2]]


@pytest.fixture
def dicaugment_bboxes():
    return [
        [0.15, 0.12, 0.20, 0.75, 0.30, 0.40, 1],
        [0.55, 0.25, 0.50, 0.90, 0.90, 0.8, 2],
    ]


@pytest.fixture
def keypoints():
    return [[20, 30, 35, 40, 50, 1], [20, 30, 40, 60, 80, 2]]


@pytest.fixture
def float_image():
    return np.random.uniform(low=0.0, high=1.0, size=(100, 100, 100)).astype("float32")


# @pytest.fixture
# def template():
#     return np.random.randint(low=0, high=256, size=(100, 100, 3), dtype=np.uint8)


# @pytest.fixture
# def float_template():
#     return np.random.uniform(low=0.0, high=1.0, size=(100, 100, 3)).astype("float32")


@pytest.fixture(scope="package")
def mp_pool():
    # Usage of `fork` as a start method for multiprocessing could lead to deadlocks on macOS.
    # Because `fork` was the default start method for macOS until Python 3.8
    # we had to manually set the start method to `spawn` to avoid those issues.
    if sys.platform == "darwin":
        method = "spawn"
    else:
        method = None
    return multiprocessing.get_context(method).Pool(8)
