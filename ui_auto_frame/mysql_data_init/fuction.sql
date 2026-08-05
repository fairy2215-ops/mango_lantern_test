-- 如果存储过程已存在，则先删除
DROP PROCEDURE IF EXISTS INIT_WAREHOUSE_AREA;

-- 创建新的存储过程
CREATE PROCEDURE INIT_WAREHOUSE_AREA()
BEGIN
    -- 初始化计数器
    SET @i = 1;

    -- 循环插入 6 条仓库数据
    WHILE @i <= 6 DO
        -- 生成仓库编号和名称
        SET @warehouse_no  = CONCAT('TEST-WH-', LPAD(@i, 3, '0'));    -- 如 TEST-WH-001
        SET @warehouse_name = CONCAT('TEST-仓库', LPAD(@i, 3, '0'));
        SET @remark        = CONCAT('仓库备注-', LPAD(@i, 3, '0'));

        -- 插入数据到 wms_warehouse 表
        INSERT INTO wms_warehouse (
            warehouse_no,
            warehouse_name,
            del_flag,
            remark,
            create_by,
            update_by,
            create_time,
            update_time
        ) VALUES (
            @warehouse_no,
            @warehouse_name,
            0,
            @remark,
            NULL,
            NULL,
            NOW(),
            NOW()
        );

        -- 只创建5个关联的库区
        IF @i < 6 THEN
            -- 获取刚插入的仓库 ID
            SET @last_warehouse_id = LAST_INSERT_ID();

            -- 生成库区信息
            SET @area_no      = CONCAT('TEST-AREA-', LPAD(@i, 3, '0'));  -- 如 TEST-AREA-001
            SET @area_name    = CONCAT('TEST-库区', LPAD(@i, 3, '0'));
            SET @area_remark  = CONCAT('库区备注-', LPAD(@i, 3, '0'));

            -- 插入数据到 wms_area 表
            INSERT INTO wms_area (
                area_no,
                area_name,
                warehouse_id,
                del_flag,
                remark,
                create_by,
                update_by,
                create_time,
                update_time
            ) VALUES (
                @area_no,
                @area_name,
                @last_warehouse_id,
                0,
                @area_remark,
                NULL,
                NULL,
                NOW(),
                NOW()
            );
        END IF;

        SET @i = @i + 1;
    END WHILE;
END