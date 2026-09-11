import os
from glob import glob

from setuptools import find_packages, setup


package_name = 'open_manipulator_tf_examples'


setup(
    name=package_name,
    version='0.1.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages', ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name, 'launch'), glob('launch/*.launch.py')),
        (os.path.join('share', package_name, 'config'), glob('config/*.yaml')),
        (os.path.join('share', package_name, 'urdf'), glob('urdf/*.xacro')),
        (os.path.join('share', package_name, 'rviz'), glob('rviz/*.rviz')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='student',
    maintainer_email='student@example.com',
    description='OpenManipulator-X TF2 and RViz2 reference examples for Physical AI Lv.1',
    license='Apache-2.0',
    entry_points={
        'console_scripts': [
            'ex_camera_static_broadcaster = open_manipulator_tf_examples.ex_camera_static_broadcaster:main',
            'ex_detected_object_broadcaster = open_manipulator_tf_examples.ex_detected_object_broadcaster:main',
            'ex_object_marker = open_manipulator_tf_examples.ex_object_marker:main',
        ],
    },
)
