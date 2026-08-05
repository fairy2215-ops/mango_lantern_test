-- 如果已存在该存储过程，则先删除
DROP PROCEDURE IF EXISTS DESTROY;

-- 创建新的存储过程
CREATE PROCEDURE DESTROY()
BEGIN
    -- 删除以 'TEST-' 开头的测试仓库数据
    DELETE FROM wms_warehouse WHERE warehouse_no LIKE 'TEST-%';

    -- 删除以 'TEST-' 开头的测试库区数据
    DELETE FROM wms_area WHERE area_no LIKE 'TEST-%';

    -- 删除以 'TEST-' 开头的测试物料分类数据
    DELETE FROM wms_item_type WHERE type_name LIKE 'TEST-%';

    -- 删除以 'TEST-' 开头的测试物料数据
    DELETE FROM wms_item WHERE item_name LIKE 'TEST-%';
END