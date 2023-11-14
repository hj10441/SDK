#!/usr/bin/env python
# coding: utf-8

# # 通过主数据资产ID获取伽利略运行数据
# 支持以伽利略资产主数据ID作为API的查询条件，确保数据索引的唯一性。


import pandas as pd
import matplotlib.pyplot as plt
from en_galileo_sdk.data_access.eda.eda_connector import EdaConnector
from en_galileo_sdk.data_access.eda.eda_analysis_data import EdaAnalysisData
import allure

plt.style.use('seaborn')


@allure.feature("伽利略数据获取Demo")
def test_EDA_DataAnalysis_CN():
    '''获取伽利略运行数据demo
    1.获取风场表信息
    2.获取风机表信息
    3.1获取风机DT通道数据信息
    3.2通过风机ID获取DT数据信息
    3.3通过风机ID获取时序信息数据
    4.获取SOE数据
    4.1 获取Event事件数据
    4.2 获取Tracelog数据
    '''
    with allure.step("断言获取连接不为None"):
        eda_conn = EdaConnector()
        assert eda_conn is not None

    # 1. 获取风场信息
    with allure.step("断言获取风场表信息"):
        wind_farm_list = eda_conn.get_wind_farm_list()
        df1 = pd.DataFrame(wind_farm_list)
        assert df1.shape[0] >= 1091, "风场数量应该大于等于1091"
        assert df1.shape[1] == 5, "风场列数为5列"
        assert set(["abbreviation", "wind_farm_id", "wind_farm_name", "region", "capacity"]).issubset(df1.columns)

    # 2.获取风机详情
    with allure.step("断言获取风机表信息"):
        wind_turbine_detail = eda_conn.get_wind_turbine_list(['GXYA'])['GXYA']
        df2 = pd.DataFrame(wind_turbine_detail).head(10)
        assert df2.shape[0] == 10, "风机数据量为10台"
        assert df2.shape[1] == 35, "风机列数应为35列"
        assert set(['assets_wind_turbine_id', 'assets_wind_turbine_name', 'wtg_alias',
                    'wind_farm_id', 'wind_farm_name', 'abbreviation',
                    'design_turbine_platform', 'turbine_series', 'gear_box_model',
                    'gear_box_brand', 'blade_part_id', 'blade_model', 'blade_brand',
                    'pitch_bearing_part_id', 'pitch_bearing_model', 'hub_height',
                    'main_shaft_part_id', 'main_bearing_part_id', 'digital_twin_version',
                    'uscada_alias', 'longitude', 'latitude', 'altitude',
                    'yaw_caliper_monent', 'sign_time_240', 'design_turbine_warranty_due',
                    'design_component_warranty_due', 'greenwich_wtg_id',
                    'pitch_bearing1_sn', 'pitch_bearing2_sn', 'pitch_bearing3_sn',
                    'nbs_part_id', 'generator_part_id', 'ngb_part_id', 'gearbox_sn']).issubset(df2.columns)

    # 3.1 获取DigitalTwin通道信息
    with allure.step("断言DT通道表信息"):
        channel_list = eda_conn.get_channel_list(name='PTH%')
        df3 = pd.DataFrame(channel_list)
        assert df3.shape[0] >= 108, "以PTH开头的DT通道应大于等于108条"
        assert df3.shape[1] == 5, "应当有5列"
        assert set([]).issubset(df3.columns)

    # 3.2 获取DigitalTwin数据
    with allure.step("断言DT类型数据信息"):
        wind_farm_turbine_dict = {'CN-53/14': ['CN-53/14-B-032']}
        start_time = "2020-11-25 00:00:00"
        end_time = "2020-11-30 00:00:00"
        channel_list = ['Stat_PitchAngle1Max', 'Stat_PitchAngle1Min', 'Stat_PitchAngle1Ave', 'Stat_SHubMx_1P',
                        'Stat_SHubMx_2P']

        eda_obj = EdaAnalysisData(eda_conn, wind_farm_turbine_dict, start_time, end_time)

        #  3.2 获取统计数据

        dt_statistics_data = eda_obj.get_dt_statistics_data(channel_list)
        df4 = pd.DataFrame(dt_statistics_data['CN-53/14']['CN-53/14-B-032'])

        # 3.3 获取时序数据

        channel_1s_list = ['PRE_YawCmdCCW', 'PRE_BR1My', 'PRE_BR2EdgeBM', 'PRE_IPC_Sensor2_NoChange', 'PRE_BR1Mx',
                           'BLE_TCA_Measure_Delta',
                           'PRE_giBPLevel', 'YAW_OverSpeedCnt']
        dt_timeseries_data = eda_obj.get_dt_timeseries_data(channel_1s_list)
        df5 = pd.DataFrame(dt_timeseries_data['CN-53/14']['CN-53/14-B-032'])

        assert df4.shape[0] == 709, "应当有709条数据"  # 生产环境这个时间段数据已经固定，数据量非特殊情况无变化
        assert df4.shape[1] == 6, "应当有6个通道"
        assert set(['plc_time', 'Stat_SHubMx_1P', 'Stat_SHubMx_2P', 'Stat_PitchAngle1Max',
                    'Stat_PitchAngle1Min', 'Stat_PitchAngle1Ave']).issubset(df4.columns)

        assert df5.shape[0] == 421177, "应当有421177条数据"  # 生产环境这个时间段数据已经固定，数据量非特殊情况无变化
        assert df5.shape[1] == 8, "应当有8个通道"
        assert set(channel_1s_list).issubset(df5.columns)

    # 4.获取SOE数据

    # 4.1 获取Event事件数据
    with allure.step("获取Event事件数据"):
        event_data = eda_obj.get_event_data(start_time='2020-04-25 00:00:00', end_time='2020-05-30 00:00:00')
        df6 = pd.DataFrame(event_data)
        assert df6.shape[0] == 44, "应当有44条数据"  # 生产环境这个时间段数据已经固定，数据量非特殊情况无变化
        assert df6.shape[1] == 16, "应当有16个通道"
        assert set(['PLC Time', 'Wind Farm Time', 'Wind Speed', 'Power', 'Generator Speed',
                    'Pitch Angle', 'Trace Log', 'wind_farm', 'turbine', 'SC Code',
                    'SC Name', 'SC Des', 'Event Type', 'Sub System', 'level', 'SC Flag']).issubset(df6.columns)

    # 4.2 获取Tracelog数据
    with allure.step("获取Tracelog数据"):
        tracelog_data = eda_obj.get_tracelog(event_data[16:17])
        df7 = pd.DataFrame(tracelog_data[0]['Trace Log Data'])
        assert df7.shape[0] == 960, "应当有960条数据"  # 生产环境这个时间段数据已经固定，数据量非特殊情况无变化
        assert df7.shape[1] == 722, "应当有722个通道"
        assert set(['PlcTime', 'gbDQ_NacelleStartYawCW', 'gbDQ_NacelleStartYawCCW',
                    'gbDI_NacelleFuseHeaterYawMotors',
                    'gbDI_NacelleFuseElectricalMotorbrakeYaw',
                    'gbDI_NacelleMotorProtYawMotorsGroup', 'gbDI_NacelleMotorProtYawMotor1',
                    'gbDI_NacelleMotorProtYawMotor2', 'gbDI_NacelleMotorProtYawMotor3',
                    'gbDI_NacelleMotorProtYawMotor4', 'gbDI_NacelleMotorProtYawMotor5',
                    'gbDI_NacelleMotorProtYawMotor6', 'gbDI_NacelleCableTwist_CW_MAX1',
                    'gbDI_NacelleCableTwist_CCW_MAX1', 'gbDI_NacelleCableTwist_CW_MAX2',
                    'gbDI_NacelleCableTwist_CCW_MAX2', 'gbDI_TowerYawCW',
                    'gbDI_TowerYawCCW', 'gbDI_NacelleYawCW', 'gbDI_NacelleYawCCW',
                    'gbDI_NacelleYawBridgeLimitSwitchCableTwist', 'gbDI_TempYawMotor1',
                    'gbDI_TempYawMotor2', 'gbDI_TempYawMotor3', 'gbDI_TempYawMotor4',
                    'gbDI_TempYawMotor5', 'gbDI_TempYawMotor6',
                    'gbDQ_NacelleOpenElectricalYawBrake', 'gbDQ_NacelleYawHeaterMotors',
                    'gbEnvisionCVT_OldFaultCode', 'bEnvisionCVT_ReadError', 'gbCVT_Rdy_RUN',
                    'gbCVT_Rdy_REF', 'gbCVT_Tripped', 'gbCVT_SpeedOK', 'gbCVT_Alarm',
                    'gbCVT_P_Limit', 'gbCVT_Q_Limit', 'gbCVT_GridFailure',
                    'gbCVT_CrowbarActive', 'gbCVT_Rdy_REF_LowSpeed',
                    'gbCVT_Rdy_RUN_LowSpeed', 'gbCVT_LifeSign_fb', 'gbCVT_Conv_P_Limit',
                    'gbCVT_EmergencySTOP', 'gbCVT_CBTripped', 'gbCVT_CBActive',
                    'gbCVT_P_OutOfRange', 'gbCVT_UPS_low', 'gbCVT_LVRT_Active',
                    'gbCVT_HeatingMode', 'gbCVT_GridOverVoltage', 'gbCVT_OK',
                    'gbConverterMachineSideRdy', 'gbCVT_Rdy_ON', 'gbCVT_Rdy_Grid',
                    'gbConverter_ServiceMode', 'gbCVT_RUN_NetSideInv', 'gbCVT_RUN_LowSpeed',
                    'gbCVT_RUN', 'gbCVT_Reset', 'gbCVT_ON', 'gbCANConverterDisturbedLevel1',
                    'gbCANConverterDisturbedLevel2', 'gbCVT_DCLinkCharged',
                    'DQ_TowerResetMCBConverter', 'gbCVT_T_S_Select', 'gbCVTSDOTimeOut',
                    'DQ_PowerResetConverter', 'DQ_NacelleValve1RotorBrakeON_sudden',
                    'DQ_NacelleValve3RotorBrakeOFF_sudden', 'DQ_bHSRotBrkValveBrk',
                    'DQ_bHSRotBrkValveRel', 'DQ_Gen1RotorBrake1', 'DQ_Gen1RotorBrake2',
                    'DQ_NacelleHydrPump', 'gbDI_NacelleRotorBrakePadsSTOP',
                    'gbDI_NacelleRotorBrakePadsAlarm', 'gbDI_NacelleHydrPump_ON_OFF',
                    'gbDI_NacelleRotorBrakeOpen', 'gbDI_NacelleMotorProtHydrPump',
                    'RemCmdACK_bEnableHSBrkPumpManualCtrl', 'gbDI_HYDSumpLevel',
                    'gbDI_NacelleMotorProtGearOilPump', 'gbDI_NacelleMotorProtGearHeater',
                    'gbDI_NacelleMotorProtGearFan', 'gbDI_NacelleGearOilLevelOK',
                    'DQ_NacelleGearFanHS', 'DQ_NacelleGearFanLS', 'DQ_NacelleGearOilPumpLS',
                    'DQ_NacelleGearOilPumpHS', 'DQ_NacelleGearHeaterOilPump',
                    'DQ_NacelleGearHeaterGearOil', 'DQ_NacelleGearHeaterFan',
                    'DQ_NacelleGearOilFilter', 'DQ_NacelleLampBypassFeatherLimitSwitch',
                    'DQ_NacelleHeaterCabinet', 'DI_NacelleRotorImpulses1',
                    'DI_NacelleRotorImpulses2', 'DI_NacelleGeneratorImpulses', 'DI_NacelleGenImpulses2',
                    'DQ_MainBearingLubON',
                    'DQ_NacelleManResetPCHVibrationMonitor',
                    'DQ_NacelleManRestartPCHVibrationMonitor',
                    'di_SafetyChainNacelleVibrationSwitch',
                    'di_SafetyChainNacelleSSDSwitch', 'DQ_TCS_Pump1Run', 'DQ_TCS_Pump2Run',
                    'DQ_TCS_InsideFan1Run', 'DQ_TCS_InsideFan2Run', 'DQ_TCS_Cooler1FansRun',
                    'DQ_TCS_Cooler2FansRun', 'DQ_TCS_Cooler3FansRun',
                    'DQ_TCS_Cooler4FansRun', 'DQ_CS_Pump1Low', 'DQ_CS_Pump1High',
                    'DQ_CS_Pump2Low', 'DQ_CS_Pump2High', 'giBPLevel',
                    'giTurbineOperationMode', 'giPowerCurveState', 'grPowerLimitByWindFarm',
                    'grCableTwistTotal', 'grYawPosition', 'giYPLevel',
                    'grActivePower_PowerMeasurement', 'grApparentPowerForProcess',
                    'grReactivePowerForProcess', 'grCosPhiForProcess',
                    'grGridFrequencyForProcess', 'grUL1L2ForProcess', 'grUL2L3ForProcess',
                    'grUL3L1ForProcess', 'grIL1ForProcess', 'grIL2ForProcess',
                    'grIL3ForProcess', 'grCVT_GenSpeed_Observer', 'grCVT_ActualTorque',
                    'grCVT_TorqueSetPointValue', 'grConverter_GridVoltage',
                    'grConverter_DClinkVoltage', 'gwConverterFaultNumber',
                    'giEnvisionCVT_FaultClassification', 'giEnvisionCVT_FaultCode',
                    'grConverter_TempHeatSink', 'giCVT_InitStatus', 'giCVTState',
                    'grNetSideCounter', 'grGenSideCounter', 'grTempGenBearingDE1',
                    'grTempGenBearingDE2', 'grTempGenBearingNDE1', 'grTempGenBearingNDE2',
                    'grTempGenStatorU1', 'grTempGenStatorU2', 'grTempGenStatorV1',
                    'grTempGenStatorV2', 'grTempGenStatorW1', 'grTempGenStatorW2',
                    'grCVT_MotorCurrent', 'grCVT_GridCurrent', 'grCVT_Pgrid',
                    'rReactivePowerSetPointValue', 'grCVT_SpeedSetPointValue',
                    'grVaneDirection', 'grWindDirection', 'grWindSpeed', 'grTempNacelle',
                    'grTempOutdoor', 'grHydrPressurePreCharge',
                    'grGearOilPressureFilterInlet', 'grGearOilPressureGBXInlet',
                    'grTempGearBearingDE', 'grTempGearBearingNDE', 'grGenSpeedPDM1',
                    'grGenSpeedPDM2', 'grRotorSpeedPDM1', 'grRotorSpeedPDM2',
                    'grGenspeedforprocess', 'grTempRotorBearing1', 'grTempRotorBearing2',
                    'grTempRearMainBearing1', 'grTempRearMainBearing2',
                    'grRotorSpeedFromOverspeedRelay', 'grTempCabinetNacelle',
                    'grTempCabinetTowerBase', 'grTempTowerBase', 'grSSDValue_PCH',
                    'grCurrentAccelerationY', 'grCurrentAccelerationX',
                    'grFilteredVibrationOmniDirection_PCH',
                    'grFilteredVibrationForeaftDirection_PCH', 'grCurrentVibrationRAW3_PCH',
                    'grCurrentVibrationRAW4_PCH', 'grTCS_WaterInletTempSetpoint',
                    'grTCS_WaterInletTempAlarm_SC2', 'grTCS_MixingValveSetpoint',
                    'grTCS_MixingValvePosition', 'grTCS_InsideCoolerInletTemp',
                    'grTCS_WaterCoolingInletTemp', 'grTCS_CVTOutletTemp', 'grTCS_TrafoOutletTemp', 'grTCS_OutletTemp',
                    'grTCS_OutsideTowerTemp', 'grTCS_PumpInletPressure',
                    'grTCS_PumpOutletPressure', 'grTCS_OutsideTowerHumidity',
                    'grTCS_CabinetFloorHumidity', 'grTCS_MixingValvePosition#1',
                    'grCCC_Temp', 'grCS_PumpOutletTemp', 'grCS_GENOutletTemp',
                    'grCS_GBXOutletTemp', 'grCS_PumpInletPressure',
                    'grCS_PumpOutletPressure', 'gr_PTH_MotorTemp_Blade1',
                    'gr_PTH_AxisBoxTemp_Blade1', 'gr_PTH_CapsTemp_Blade1',
                    'gr_PTH_InverterTemp_Blade1', 'di_PTH_EndPos95Deg_Blade1',
                    'gr_PTH_PitchSpeed_Blade1', 'gr_PTH_MotorCurrent_Blade1',
                    'gr_PTH_CapVoltage_Blade1', 'gr_PTH_PitchAngle_Blade1',
                    'gr_PTH_AngleSetValueFinal_Blade1', 'gr_PTH_ImbalanceOffset_Blade1',
                    'gb_PTH_BrakeLock_Blade1', 'gr_PTH_MotorTemp_Blade2',
                    'gr_PTH_AxisBoxTemp_Blade2', 'gr_PTH_CapsTemp_Blade2',
                    'gr_PTH_InverterTemp_Blade2', 'di_PTH_EndPos95Deg_Blade2',
                    'gr_PTH_PitchSpeed_Blade2', 'gr_PTH_MotorCurrent_Blade2',
                    'gr_PTH_CapVoltage_Blade2', 'gr_PTH_PitchAngle_Blade2',
                    'gr_PTH_AngleSetValueFinal_Blade2', 'gr_PTH_ImbalanceOffset_Blade2',
                    'gb_PTH_BrakeLock_Blade2', 'gr_PTH_MotorTemp_Blade3',
                    'gr_PTH_AxisBoxTemp_Blade3', 'gr_PTH_CapsTemp_Blade3',
                    'gr_PTH_InverterTemp_Blade3', 'di_PTH_EndPos95Deg_Blade3',
                    'gr_PTH_PitchSpeed_Blade3', 'gr_PTH_MotorCurrent_Blade3',
                    'gr_PTH_CapVoltage_Blade3', 'gr_PTH_PitchAngle_Blade3',
                    'gr_PTH_AngleSetValueFinal_Blade3', 'gr_PTH_ImbalanceOffset_Blade3',
                    'gb_PTH_BrakeLock_Blade3', 'DQ_PTH_EFCSigOutput', 'grTempGearOilSump',
                    'grNacelleTotalCurrent', 'grYawMotorSpeedPDM1', 'grTempInnerYawMotor1',
                    'grTempInnerYawMotor2', 'grTempInnerYawMotor3', 'grTempInnerYawMotor4',
                    'grTempGearOilInlet', 'grTempGearBearingInterNDE_1min',
                    'grTempGearBearingInterDE_1min', 'grGearboxBearing_IMS_RS_Temp_1min',
                    'grGearboxBearing_IMS_GSRS_Temp_1min',
                    'grGearboxBearing_IMS_GSGS_Temp_1min',
                    'grGearboxBearing_HSS_RS_Temp_1min',
                    'grGearboxBearing_HSS_GSRS_Temp_1min',
                    'grGearboxBearing_HSS_GSGS_Temp_1min', 'grFrontYawPadDistance',
                    'grBackYawPadDistance', 'grCVT_ReactivePowerSetPointValue',
                    'grAVCIn_AutoTerminalVoltageCmdFromEMS',
                    'grReactiveCompensationSetPointValue', 'grConverter_GridVoltage#1',
                    'grAVCout_ReactivePower', 'grAVC_Trip',
                    'gbDI_NacelleMotorProtYawMotor7', 'gbDI_NacelleMotorProtYawMotor8',
                    'gbDI_TempYawMotor7', 'gbDI_TempYawMotor8',
                    'gbDI_NacelleYawAutoGreaseOilLevelLow',
                    'gbDI_NacelleYawAutoGreaseOilBlock', 'gbDI_Yaw_Lub_MCB',
                    'gbDQ_NacelleAutoGrease', 'gbDI_YawLubrication2FrictionPlate_GreaseLow',
                    'gbDI_YawLubrication2FrictionPlate_GreaseBlock',
                    'gbDI_YawLubrication2FrictionPlate_MCB',
                    'gbDQ_YawLubrication2FrictionPlate', 'gbEnableLaserClearanceControl',
                    'grLaserClearanceValue', 'gbEnableMWClearanceControl',
                    'grBladeClearance_Fit', 'gbEnableIBCClearanceControl',
                    'grBladeClearance_Fit_IBC', 'grCounterFromConverter',
                    'gbFineBoost_ActFlag', 'gbTrans_PLimFlag', 'gbRotorIlimFlag',
                    'gbStatorIlimFlag', 'gbI_Lsc_LimFlag', 'grFineBoost_Trans_Ifbk', 'grFineBoost_Is_Actual',
                    'grFineBoost_Ir_Actual', 'grFineBoost_ILsc_Actual', 'grI_Lsc_Lim_Rate',
                    'grStator_IRate', 'grRotor_IRat', 'grTrans_IRat', 'grTrans_UbaseIlim',
                    'grTransCable_IRat', 'grCable_Stator_IRat', 'grGen_Stator_IRat',
                    'grGen_Rotor_I', 'grCable_Rotor_IRat', 'grConv_Rotor_IRat',
                    'grFineBoost_EDStatus', 'grFineBoost_TorqueLim', 'grCableTemperature1',
                    'grCableTemperature2', 'grWindSpeedVectorXOrignal',
                    'grWindSpeedVectorYOrignal', 'grWindSpeedVectorZOrignal',
                    'grWindSpeedOrignal', 'grFocalDistance', 'gbHeartBitFromLadarDisturbe',
                    'gbHeartBitFromLadar', 'gb_PTH_EFCSigFeedBack',
                    'gbDI_SafetyChainHumanFeedback',
                    'gbDI_SafetyChainHumanNacelleOL24VOutputs',
                    'gbDI_SafetyChainMachineFeedback',
                    'gbDI_SafetyChainNacelleRelayOverspeed',
                    'gbDI_TowerFeedback24VOutputSafetyChainHuman',
                    'gbDI_UnderspeedRelayFault', 'DQ_SafetyChainOpenByPLC',
                    'DQ_SafetyChainResetByPLC', 'DQ_SafetyChainResetRelayOverspeed',
                    'DQ_OverSpeedRelayReboot', 'gbDI_SafetyChainTowerEmergencySTOP',
                    'gbDI_SafetyChainNacelleEmergencySTOP', 'gbBP160Flag_CoreCtrl',
                    'dq_PTH_StartSpclMode', 'bSafPos2SetCmdGridloss', 'grRawRotorSpeedPDM1',
                    'grRawRotorSpeedPDM2', 'grRawGenSpeedPDM2', 'grRawGenSpeedPDM1',
                    'gb_PTH_CommOK', 'GenSpdSet', 'AngleSet1', 'AngleSet2', 'AngleSet3',
                    'grSpeedReduction_ToEnvision', 'grPowerReduction_ToEnvision',
                    'grPitchAngleReduction_ToEnvision', 'gbDI_TowerThermostatsProt',
                    'gbDI_NacelleThermostatsProt',
                    'gbDI_NacellePowerSupply24VDC_TheOtherLoad',
                    'gbDI_NacellePowerSupply24VDC_HumanSafetyLoad',
                    'gbDI_NacelleCabinetOutIO_24VDCSuplly',
                    'gbDI_NacelleCabinetInIO_24VDCSuplly',
                    'gbDI_TowerUPS24VPLC_BatteryMode', 'gbDI_230VMCB', 'gbDI_UPS230VMCB',
                    'gbDI_TowerBaseCabinetOutIO_24VDCSuplly',
                    'gbDI_TowerBaseCabinetInIO_24VDCSuplly', 'grDTF_VibRMS',
                    'gb_DQ_MainBearingLubHeaterON', 'grTempGearbox_OilCoolerOutlet',
                    'gbDI_GearFilterBlocking', 'gbDI_NacelleRotorBoltLocked',
                    'gbDI_RotorLock_Pin1Locked', 'gbDI_RotorLock_Pin2Locked',
                    'gbDI_RotorLock_Pin1UnLocked', 'gbDI_RotorLock_Pin2UnLocked',
                    'gbDI_OverspeedRelayFault', 'grTransformer_Temp',
                    'grTransformerWindingTemp', 'grTransformerAuxiliaryWindingTemp',
                    'grCableTemperature1#1', 'grCableTemperature2#1',
                    'grTempGenSlipRingInside', 'grAI_AirInletPressureDiff',
                    'gbDI_YawContactorClose', 'STMBladeReached85', 'gbDQ_ACS_FanStart',
                    'giState', 'gbFIDAutoRecoveryOn', 'gbAutoRecoveryReset',
                    'gbMAIN_ResetSafetyChain', 'gbMAIN_ResetSubsystem',
                    'gbMAIN_ResetStatusCodes', 'grTempPlanetRearBearing1',
                    'grTempPlanetRearBearing2', 'grTempPlanetRearBearing3',
                    'DQ_KEB_IntoNormalMode_Blade1', 'DQ_KEB_IntoEmergencyMode_Blade1',
                    'DQ_KEB_PCUResetCmd_Blade1', 'DQ_KEB_CapDischargeCmd_Blade1',
                    'DQ_KEB_PowerSupplyCutoffCmd_Blade1', 'DQ_KEB_ChgSpdCmd_Blade1', 'DQ_KEB_StartSpclMode_Blade1',
                    'DQ_KEB_91DegResetCmd_Blade1',
                    'AQ_KEB_CommCounter_Blade1', 'AQ_KEB_PTHSpdSetValue_Blade1',
                    'gb_KEB_Limit91WrongPos_Blade1', 'gb_KEB_Limit95WrongPos_Blade1',
                    'dq_KEB_DischargeCapBP170_Blade1', 'gb_KEB_CapSelftestStart_Blade1',
                    'gb_KEB_PitchingStart_Blade1', 'gr_KEB_AngleSetValueSelftest_Blade1',
                    'gr_KEB_CapVoltageAtSelftestStart_Blade1',
                    'gb_KEB_SelftestSafetyRunStart_Blade1',
                    'gr_KEB_CapVoltageAtSelftestStop_Blade1', 'gb_KEB_ReachZeroPos_Blade1',
                    'DQ_KEB_IntoNormalMode_Blade2', 'DQ_KEB_IntoEmergencyMode_Blade2',
                    'DQ_KEB_PCUResetCmd_Blade2', 'DQ_KEB_CapDischargeCmd_Blade2',
                    'DQ_KEB_PowerSupplyCutoffCmd_Blade2', 'DQ_KEB_ChgSpdCmd_Blade2',
                    'DQ_KEB_StartSpclMode_Blade2', 'DQ_KEB_91DegResetCmd_Blade2',
                    'AQ_KEB_CommCounter_Blade2', 'AQ_KEB_PTHSpdSetValue_Blade2',
                    'gb_KEB_Limit91WrongPos_Blade2', 'gb_KEB_Limit95WrongPos_Blade2',
                    'dq_KEB_DischargeCapBP170_Blade2', 'gb_KEB_CapSelftestStart_Blade2',
                    'gb_KEB_PitchingStart_Blade2', 'gr_KEB_AngleSetValueSelftest_Blade2',
                    'gr_KEB_CapVoltageAtSelftestStart_Blade2',
                    'gb_KEB_SelftestSafetyRunStart_Blade2',
                    'gr_KEB_CapVoltageAtSelftestStop_Blade2', 'gb_KEB_ReachZeroPos_Blade2',
                    'DQ_KEB_IntoNormalMode_Blade3', 'DQ_KEB_IntoEmergencyMode_Blade3',
                    'DQ_KEB_PCUResetCmd_Blade3', 'DQ_KEB_CapDischargeCmd_Blade3',
                    'DQ_KEB_PowerSupplyCutoffCmd_Blade3', 'DQ_KEB_ChgSpdCmd_Blade3',
                    'DQ_KEB_StartSpclMode_Blade3', 'DQ_KEB_91DegResetCmd_Blade3',
                    'AQ_KEB_CommCounter_Blade3', 'AQ_KEB_PTHSpdSetValue_Blade3',
                    'gb_KEB_Limit91WrongPos_Blade3', 'gb_KEB_Limit95WrongPos_Blade3',
                    'dq_KEB_DischargeCapBP170_Blade3', 'gb_KEB_CapSelftestStart_Blade3',
                    'gb_KEB_PitchingStart_Blade3', 'gr_KEB_AngleSetValueSelftest_Blade3',
                    'gr_KEB_CapVoltageAtSelftestStart_Blade3',
                    'gb_KEB_SelftestSafetyRunStart_Blade3',
                    'gr_KEB_CapVoltageAtSelftestStop_Blade3', 'gb_KEB_ReachZeroPos_Blade3',
                    'di_KEB_StandbyMode_Blade1', 'di_KEB_TeachedOperationFinished_Blade1',
                    'di_KEB_FeatherPositionReached_Blade1',
                    'di_KEB_ModulationActive_Blade1',
                    'di_KEB_MainPowerSupplyFailure_Blade1',
                    'di_KEB_EncoderResetFinished_Blade1', 'di_KEB_InverterWarning_Blade1',
                    'di_KEB_InverterFanError_Blade1', 'di_KEB_HeatsinkFanError_Blade1',
                    'di_KEB_HeatsinkTempWarn_Blade1', 'di_KEB_InverterTempWarn_Blade1',
                    'di_KEB_MotorTempWarn_Blade1', 'di_KEB_LightningProtectOff_Blade1',
                    'di_KEB_MotorTempWireBreak_Blade1', 'di_KEB_MotorBrakeWireBreak_Blade1',
                    'di_KEB_PhaseFailure_Blade1', 'di_KEB_CapsOverVoltageWarn_Blade1',
                    'di_KEB_DCFuseTrip_Blade1', 'di_KEB_TargetPosSyncError_Blade1',
                    'di_KEB_SensorDefect_3Deg_Blade1', 'di_KEB_SensorDefect_88Deg_Blade1',
                    'di_KEB_CapsUnderVoltageError_Blade1',
                    'di_KEB_CapsChargeLoopsError_Blade1', 'di_KEB_CapsChargingError_Blade1',
                    'di_KEB_SafetyChainTrigger_Blade1', 'di_KEB_MotorStall_Blade1',
                    'di_KEB_MotorCableBroken_Blade1',
                    'di_KEB_LimitSwitch88Incoherence_Blade1',
                    'di_KEB_LimitSwitch95Incoherence_Blade1',
                    'di_KEB_InverterCommError_Blade1', 'di_KEB_InverterError_Blade1',
                    'di_KEB_MotorEncoderError_Blade1', 'di_KEB_OverSpeedError_Blade1',
                    'di_KEB_FieldbusCommError_Blade1', 'di_KEB_24VOutputOverload_Blade1',
                    'di_KEB_EmergencyByFieldbus_Blade1', 'di_KEB_LVRT_Blade1',
                    'di_KEB_NegativeLimitSwitch_Blade1', 'di_KEB_PowerSupplyF1Trip_Blade1',
                    'di_KEB_EFCNotReceivedByPTH_Blade1', 'di_KEB_13Q1Trip_Blade1',
                    'di_KEB_91DegCheckAlarm_Blade1', 'di_KEB_EndPos91Deg_Blade1',
                    'di_KEB_SpecialMode_Blade1', 'gr_KEB_SAFRunSpd1_Blade1',
                    'gr_KEB_SAFRunSpd2_Blade1', 'gr_KEB_SAFRunSpd3_Blade1', 'gr_KEB_SAFRunPos1_Blade1',
                    'gr_KEB_SAFRunPos2_Blade1', 'di_KEB_StandbyMode_Blade2',
                    'di_KEB_TeachedOperationFinished_Blade2',
                    'di_KEB_FeatherPositionReached_Blade2',
                    'di_KEB_ModulationActive_Blade2',
                    'di_KEB_MainPowerSupplyFailure_Blade2',
                    'di_KEB_EncoderResetFinished_Blade2', 'di_KEB_InverterWarning_Blade2',
                    'di_KEB_InverterFanError_Blade2', 'di_KEB_HeatsinkFanError_Blade2',
                    'di_KEB_HeatsinkTempWarn_Blade2', 'di_KEB_InverterTempWarn_Blade2',
                    'di_KEB_MotorTempWarn_Blade2', 'di_KEB_LightningProtectOff_Blade2',
                    'di_KEB_MotorTempWireBreak_Blade2', 'di_KEB_MotorBrakeWireBreak_Blade2',
                    'di_KEB_PhaseFailure_Blade2', 'di_KEB_CapsOverVoltageWarn_Blade2',
                    'di_KEB_DCFuseTrip_Blade2', 'di_KEB_TargetPosSyncError_Blade2',
                    'di_KEB_SensorDefect_3Deg_Blade2', 'di_KEB_SensorDefect_88Deg_Blade2',
                    'di_KEB_CapsUnderVoltageError_Blade2',
                    'di_KEB_CapsChargeLoopsError_Blade2', 'di_KEB_CapsChargingError_Blade2',
                    'di_KEB_SafetyChainTrigger_Blade2', 'di_KEB_MotorStall_Blade2',
                    'di_KEB_MotorCableBroken_Blade2',
                    'di_KEB_LimitSwitch88Incoherence_Blade2',
                    'di_KEB_LimitSwitch95Incoherence_Blade2',
                    'di_KEB_InverterCommError_Blade2', 'di_KEB_InverterError_Blade2',
                    'di_KEB_MotorEncoderError_Blade2', 'di_KEB_OverSpeedError_Blade2',
                    'di_KEB_FieldbusCommError_Blade2', 'di_KEB_24VOutputOverload_Blade2',
                    'di_KEB_EmergencyByFieldbus_Blade2', 'di_KEB_LVRT_Blade2',
                    'di_KEB_NegativeLimitSwitch_Blade2', 'di_KEB_PowerSupplyF1Trip_Blade2',
                    'di_KEB_EFCNotReceivedByPTH_Blade2', 'di_KEB_13Q1Trip_Blade2',
                    'di_KEB_91DegCheckAlarm_Blade2', 'di_KEB_EndPos91Deg_Blade2',
                    'di_KEB_SpecialMode_Blade2', 'gr_KEB_SAFRunSpd1_Blade2',
                    'gr_KEB_SAFRunSpd2_Blade2', 'gr_KEB_SAFRunSpd3_Blade2',
                    'gr_KEB_SAFRunPos1_Blade2', 'gr_KEB_SAFRunPos2_Blade2',
                    'di_KEB_StandbyMode_Blade3', 'di_KEB_TeachedOperationFinished_Blade3',
                    'di_KEB_FeatherPositionReached_Blade3',
                    'di_KEB_ModulationActive_Blade3',
                    'di_KEB_MainPowerSupplyFailure_Blade3',
                    'di_KEB_EncoderResetFinished_Blade3', 'di_KEB_InverterWarning_Blade3',
                    'di_KEB_InverterFanError_Blade3', 'di_KEB_HeatsinkFanError_Blade3',
                    'di_KEB_HeatsinkTempWarn_Blade3', 'di_KEB_InverterTempWarn_Blade3',
                    'di_KEB_MotorTempWarn_Blade3', 'di_KEB_LightningProtectOff_Blade3',
                    'di_KEB_MotorTempWireBreak_Blade3', 'di_KEB_MotorBrakeWireBreak_Blade3',
                    'di_KEB_PhaseFailure_Blade3', 'di_KEB_CapsOverVoltageWarn_Blade3',
                    'di_KEB_DCFuseTrip_Blade3', 'di_KEB_TargetPosSyncError_Blade3',
                    'di_KEB_SensorDefect_3Deg_Blade3', 'di_KEB_SensorDefect_88Deg_Blade3',
                    'di_KEB_CapsUnderVoltageError_Blade3',
                    'di_KEB_CapsChargeLoopsError_Blade3', 'di_KEB_CapsChargingError_Blade3',
                    'di_KEB_SafetyChainTrigger_Blade3', 'di_KEB_MotorStall_Blade3',
                    'di_KEB_MotorCableBroken_Blade3',
                    'di_KEB_LimitSwitch88Incoherence_Blade3',
                    'di_KEB_LimitSwitch95Incoherence_Blade3',
                    'di_KEB_InverterCommError_Blade3', 'di_KEB_InverterError_Blade3',
                    'di_KEB_MotorEncoderError_Blade3', 'di_KEB_OverSpeedError_Blade3',
                    'di_KEB_FieldbusCommError_Blade3', 'di_KEB_24VOutputOverload_Blade3',
                    'di_KEB_EmergencyByFieldbus_Blade3', 'di_KEB_LVRT_Blade3',
                    'di_KEB_NegativeLimitSwitch_Blade3', 'di_KEB_PowerSupplyF1Trip_Blade3',
                    'di_KEB_EFCNotReceivedByPTH_Blade3', 'di_KEB_13Q1Trip_Blade3',
                    'di_KEB_91DegCheckAlarm_Blade3', 'di_KEB_EndPos91Deg_Blade3',
                    'di_KEB_SpecialMode_Blade3', 'gr_KEB_SAFRunSpd1_Blade3',
                    'gr_KEB_SAFRunSpd2_Blade3', 'gr_KEB_SAFRunSpd3_Blade3',
                    'gr_KEB_SAFRunPos1_Blade3', 'gr_KEB_SAFRunPos2_Blade3', 'gr_KEB_HeatsinkTemp_Blade1_1s',
                    'gr_KEB_HeatsinkTemp_Blade2_1s', 'gr_KEB_HeatsinkTemp_Blade3_1s',
                    'di_KEB_MaintenanceMode', 'di_KEB_NormalMode_Blade1',
                    'di_KEB_NormalMode_Blade2', 'di_KEB_NormalMode_Blade3',
                    'di_KEB_EmergencyMode', 'gr_KEB_MotorTemp_Blade1',
                    'gr_KEB_MotorTemp_Blade2', 'gr_KEB_MotorTemp_Blade3',
                    'gr_KEB_CapsTemp_Blade1', 'gr_KEB_CapsTemp_Blade2',
                    'gr_KEB_CapsTemp_Blade3', 'gr_KEB_AxisBoxTemp_Blade1',
                    'gr_KEB_AxisBoxTemp_Blade2', 'gr_KEB_AxisBoxTemp_Blade3',
                    'gr_KEB_MotorCurrent_Blade1', 'gr_KEB_MotorCurrent_Blade2',
                    'gr_KEB_MotorCurrent_Blade3', 'gr_KEB_BrakeResisPeak_Blade1',
                    'gr_KEB_BrakeResisPeak_Blade2', 'gr_KEB_BrakeResisPeak_Blade3',
                    'ai_KEB_InverterErrorCode_Blade1', 'ai_KEB_InverterErrorCode_Blade2',
                    'ai_KEB_InverterErrorCode_Blade3', 'dq_KEB_SafPos2SetCmd',
                    'dq_KEB_SafPos2ResetCmd', 'gb_KEB_SafPos2SetCmdPwrUp',
                    'gb_KEB_SpecMode_165', 'gb_KEB_SpecMode_198', 'ai_KEB_HeartBeat_Blade1',
                    'ai_KEB_HeartBeat_Blade2', 'ai_KEB_HeartBeat_Blade3',
                    'dqConverter_PLCLifeSign', 'grTCS_CVTIntletTemp_1sec', 'grTCS_Humidity',
                    'grGBXTorqueArmPositionLeft_Calibration',
                    'grGBXTorqueArmPositionRight_Calibration', 'grGBXTorqueArmPositionLeft',
                    'grGBXTorqueArmPositionRight', 'CCU_IN_dALCErr', 'CCU_IPC_Sensor1',
                    'CCU_IPC_Sensor2', 'CCU_IPC_Sensor3', 'CCU_IPC_Sensor4',
                    'CCU_IPC_RotorPosDegree', 'CCU_IPC_Q_Disp', 'CCU_IPC_D_Disp',
                    'CCU_IPCon_trqSHMyFlt', 'CCU_IPCon_trqSHMzFlt', 'CCU_IPCon_degD',
                    'CCU_IPCon_degQ', 'grENVin_IPCErrorCode', 'grENVin_IPCErrorCode2',
                    'gbBoltDetectSysReady', 'gbHeartBeatFromBoltDetect',
                    'gbDI_BoltDetectMainShaftProxSwitch', 'gbDI_BoltDetectSignalBlade1',
                    'gbDI_BoltDetectSignalBlade2', 'gbDI_BoltDetectSignalBlade3',
                    'gbDI_OuterBoltDetectSignalBlade1', 'gbDI_OuterBoltDetectSignalBlade2',
                    'gbDI_OuterBoltDetectSignalBlade3', 'grWindingBTemperature',
                    'grGCCRoomTemperature', 'grTransformer_Temp_Phase1',
                    'grTransformer_Temp_Phase2', 'grTransformer_Temp_Phase3',
                    'grENVin_ErrorCode3', 'grENVin_ErrorCode4', 'CurtailCode',
                    'CCU_PTHMin_idxModule', 'gb_PTH_PTHAngleWrongPos', 'gbCVT_HVRT',
                    'grCVTGridInductorTemp_1s', 'grCVTRotorInductorTemp_1s',
                    'grCVTConvOutletTemp_1s', 'grCVTPowOutletTemp_1s',
                    'grFineBoost_TorqueLimFinal', 'grGenSpd_Std', 'CCU_WEM_Super_ErrorVal',
                    'CCU_WEM_vWindEst', 'CCU_WEM_nGenEst', 'CCU_WEM_State',
                    'gbDI_TowerBaseSmokeDetected', 'gbDI_AUXTransformer690PowerSupply',
                    'gbDI_AUXTransformer400PowerSupply', 'gbDI_NacelleGearOilFilterOK',
                    'gbDI_NacelleMotorProtGenFan', 'grRawWindSpeedFromMechanical',
                    'grRawWindSpeedFromUltraSonic', 'grCurrDirVane1Relative',
                    'grVaneDirection1_1sec', 'grVaneDirection2_1sec', 'AI_PitchAcc_Axis1X',
                    'AI_PitchAcc_Axis1Y', 'AI_PitchAcc_Axis1Z', 'AI_PitchAcc_Axis2X', 'AI_PitchAcc_Axis2Y',
                    'AI_PitchAcc_Axis2Z', 'AI_PitchAcc_Axis3X',
                    'AI_PitchAcc_Axis3Y', 'AI_PitchAcc_Axis3Z', 'di_KEB_ForceMode',
                    'di_KEB_MainPowerSupplyFailure', 'di_MGAC_EndPos95Deg_Blade1',
                    'di_MGAC_EndPos95Deg_Blade2', 'di_MGAC_EndPos95Deg_Blade3',
                    'di_MGAC_SymetryError_Blade1', 'di_MGAC_SymetryError_Blade2',
                    'di_MGAC_SymetryError_Blade3', 'gr_KEB_CapsVoltage_Blade1',
                    'gr_KEB_CapsVoltage_Blade2', 'gr_KEB_CapsVoltage_Blade3',
                    'gbLimitSwitchCableTwistCCWBridge', 'gbLimitSwitchCableTwistCWBridge',
                    'grNacellePositionTotal', 'grNacellePositionLtd', 'rYawPositionInvers',
                    'grVaneDirection_Yaw_use']).issubset(df7.columns)
