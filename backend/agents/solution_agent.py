"""SolutionAgent - 技术方案生成Agent"""
from backend.agents.base_agent import BaseAgent, AgentContext, AgentResult
from backend.models.schemas import SolutionResult, SolutionSection


class SolutionAgent(BaseAgent):
    name = "SolutionAgent"
    description = "技术方案初稿生成Agent"

    async def mock_run(self, context: AgentContext) -> AgentResult:
        text = context.tender_text
        solution = SolutionResult()

        if "智慧园区" in text:
            solution.sections = self._smart_park_solution()
        elif "数据中台" in text or "数据治理" in text:
            solution.sections = self._data_platform_solution()
        else:
            solution.sections = self._gov_service_solution()

        solution.toc = [s.title for s in solution.sections]
        solution.total_words = sum(len(s.content) for s in solution.sections)

        return AgentResult(
            agent=self.name,
            output=solution.model_dump(),
            summary=f"生成技术方案初稿，共{len(solution.sections)}个章节，约{solution.total_words}字",
            references=["software_project_solution_template.md"]
        )

    def _smart_park_solution(self):
        return [
            SolutionSection(title="1. 项目理解与需求分析", content=(
                "本项目为某市智慧园区综合管理平台建设，旨在实现园区设备统一接入、数据集中管理、"
                "可视化展示和智能运维。核心需求包括统一门户、设备接入管理、数据可视化、权限管理、"
                "日志审计、数据安全和国产化适配。项目预算480万元，建设周期90天，技术分占比60%。")),
            SolutionSection(title="2. 建设目标", content=(
                "总体目标：构建统一的智慧园区管理平台，实现设备全接入、数据全汇聚、管理可视化、运维智能化。\n"
                "具体目标：统一门户（SSO+多终端）、设备接入（200+协议）、数据可视化（实时大屏）、"
                "权限管理（RBAC细粒度）、日志审计（180天保留）、数据安全（加密脱敏）、国产化全适配。")),
            SolutionSection(title="3. 总体架构设计", content=(
                "采用微服务架构，四层设计：\n"
                "- 展示层：统一门户、数据可视化大屏、移动端\n"
                "- 业务层：设备接入服务、权限服务、审计服务、告警服务\n"
                "- 数据层：时序数据库+关系数据库+缓存\n"
                "- 基础设施层：消息队列+API网关+服务注册\n"
                "技术选型：Vue3+Spring Cloud+PostgreSQL/达梦+Redis+Kafka\n"
                "需人工确认：技术选型需结合企业技术栈确定。"), needs_review=True),
            SolutionSection(title="4. 功能模块设计", content=(
                "4.1 统一门户：SSO集成、个性化工作台、多终端适配、500+并发支持\n"
                "4.2 设备接入管理：200+协议适配（Modbus/BACnet/OPC UA/MQTT/HTTP）、"
                "自动发现注册、实时监控告警、标准API\n"
                "4.3 数据可视化：实时5秒刷新、10+可视化组件、自适应布局、数据钻取联动\n"
                "4.4 权限管理：RBAC、组织架构管理、功能+数据权限分离\n"
                "4.5 日志审计：全操作记录、不可篡改、180天保留、异常告警\n"
                "4.6 数据安全：SM4加密、脱敏规则、分类分级、等保二级\n"
                "4.7 国产化：飞腾/鲲鹏CPU+麒麟/UOS+达梦/金仓+东方通\n"
                "需人工确认：各模块详细设计需根据实际需求细化。"), needs_review=True),
            SolutionSection(title="5. 数据架构设计", content=(
                "设备数据层：时序数据库存储设备实时数据\n"
                "业务数据层：关系数据库存储业务数据\n"
                "缓存层：Redis缓存热点数据\n"
                "需人工确认：数据模型需根据实际业务设计。"), needs_review=True),
            SolutionSection(title="6. 安全体系设计", content="等保二级合规+国密算法+RBAC+审计日志+数据加密脱敏"),
            SolutionSection(title="7. 国产化适配方案", content=(
                "CPU适配：飞腾/鲲鹏（ARM架构编译优化）\n"
                "操作系统适配：银河麒麟/统信UOS（系统调用兼容）\n"
                "数据库适配：达梦/人大金仓（SQL方言+驱动适配）\n"
                "中间件适配：东方通/宝兰德（Java EE规范兼容）\n"
                "适配验证：逐项功能测试+性能测试+兼容性测试")),
            SolutionSection(title="8. 实施计划", content=(
                "项目周期90天：\n"
                "- 第1阶段（1-15天）：需求确认+架构设计+环境搭建\n"
                "- 第2阶段（16-55天）：核心模块开发（门户+设备接入+可视化）\n"
                "- 第3阶段（56-75天）：权限+审计+安全+国产化适配\n"
                "- 第4阶段（76-90天）：集成测试+培训上线\n"
                "需人工确认：计划需根据团队规模调整。"), needs_review=True),
            SolutionSection(title="9. 项目团队配置", content=(
                "项目经理1人、技术负责人1人、架构师1人、前端开发3人、后端开发4人、"
                "测试2人、运维1人\n需人工确认：人员配置需根据企业实际情况调整。"), needs_review=True),
            SolutionSection(title="10. 测试验收方案", content="功能测试+性能测试+安全测试+国产化验证+用户验收"),
            SolutionSection(title="11. 培训方案", content="培训5天，覆盖系统管理员和业务操作员"),
            SolutionSection(title="12. 运维服务方案", content="质保期1年，7x24技术支持，2小时响应"),
            SolutionSection(title="13. 风险控制方案", content="进度风险：里程碑监控+周报\n质量风险：代码评审+自动化测试\n安全风险：等保测评+安全扫描"),
        ]

    def _data_platform_solution(self):
        return [
            SolutionSection(title="1. 项目理解与需求分析", content=(
                "本项目为某区数据中台建设，旨在实现区域数据统一治理、目录管理、交换共享和质量管控。"
                "核心需求包括数据治理平台、数据目录系统、数据交换共享平台、数据质量管理系统、数据安全和标准接口。"
                "项目预算800万元，建设周期120天。")),
            SolutionSection(title="2. 建设目标", content=(
                "总体目标：构建区级数据中台，实现数据资源可见、可用、可管、可控。\n"
                "数据治理：元数据+标准+质量+资产全维度管理\n"
                "数据目录：资源编目+分类检索+申请审批\n"
                "数据交换：多源异构数据统一接入和共享\n"
                "数据质量：规则配置+自动检测+闭环处理")),
            SolutionSection(title="3. 总体架构设计", content=(
                "采用数据湖+数据仓库双层架构：\n"
                "- 数据接入层：多源数据采集（批量/实时/增量）\n"
                "- 数据治理层：元数据管理、标准管理、质量管理\n"
                "- 数据服务层：数据目录、数据交换、API服务\n"
                "- 数据安全层：加密脱敏、访问控制、审计日志\n"
                "需人工确认：技术选型需结合企业技术栈确定。"), needs_review=True),
            SolutionSection(title="4. 功能模块设计", content=(
                "4.1 数据治理平台：元数据自动采集、标准管理、资产盘点、血缘分析\n"
                "4.2 数据目录系统：资源编目、分类标签、检索预览、申请审批\n"
                "4.3 数据交换共享：10+种数据源接入、全量/增量/实时同步、任务调度\n"
                "4.4 数据质量管理：5维度检测、自定义规则、工单闭环、趋势分析\n"
                "需人工确认：各模块需根据实际数据源细化。"), needs_review=True),
            SolutionSection(title="5. 数据架构设计", content=(
                "数据分层：ODS→DWD→DWS→ADS\n遵循政务数据标准规范\n核心数据100%质量检测覆盖\n需人工确认：数据模型需根据实际业务设计。"), needs_review=True),
            SolutionSection(title="6. 安全体系设计", content="等保三级+SM4/AES256加密+静态/动态脱敏+细粒度访问控制+审计日志"),
            SolutionSection(title="7. 实施计划", content=(
                "项目周期120天：\n"
                "- 第1阶段（1-20天）：需求调研+数据源梳理+架构设计\n"
                "- 第2阶段（21-70天）：核心平台开发（治理+目录+交换）\n"
                "- 第3阶段（71-100天）：质量系统+安全模块+接口开发\n"
                "- 第4阶段（101-120天）：联调测试+数据迁移+培训上线\n"
                "需人工确认：实施计划需根据团队规模调整。"), needs_review=True),
            SolutionSection(title="8. 项目团队配置", content=(
                "项目经理1人、技术负责人1人、数据架构师2人、开发8人、数据工程师3人、测试2人、运维1人\n"
                "需人工确认：人员配置需根据企业实际情况调整。"), needs_review=True),
            SolutionSection(title="9. 测试验收方案", content="功能测试+性能测试+安全测试+等保测评+数据质量验证"),
            SolutionSection(title="10. 培训方案", content="培训8天，覆盖数据管理员、业务操作员、接口开发者"),
            SolutionSection(title="11. 运维服务方案", content="质保期2年，7x24技术支持，2小时响应"),
            SolutionSection(title="12. 风险控制方案", content="数据质量风险：规则自动检测+人工复核\n进度风险：里程碑监控\n安全风险：等保测评+安全审计"),
        ]

    def _gov_service_solution(self):
        return [
            SolutionSection(title="1. 项目理解与需求分析", content=(
                "本项目为某市政务服务一体化平台升级，旨在提升政务服务能力，优化办件流程，适配移动端。"
                "核心需求包括平台升级改造、移动端适配、办件流程优化、用户体验提升。"
                "项目预算350万元，建设周期60天。")),
            SolutionSection(title="2. 建设目标", content=(
                "总体目标：升级政务服务一体化平台，实现一网通办、移动可办、流程更优。\n"
                "移动端：iOS+Android+微信小程序全适配\n"
                "流程优化：20+高频办件优化，时限压缩30%+\n"
                "用户体验：智能导办、无障碍适配、个性化首页")),
            SolutionSection(title="3. 总体架构设计", content=(
                "在现有平台基础上升级，保持架构延续性：\n"
                "- 前端升级：响应式框架+小程序+适老化改造\n"
                "- 后端升级：微服务拆分优化+流程引擎升级\n"
                "- 移动端：uni-app跨端方案\n"
                "需人工确认：升级方案需结合现有系统技术栈。"), needs_review=True),
            SolutionSection(title="4. 功能模块设计", content=(
                "4.1 平台升级：平滑升级+统一认证对接+电子证照+事项动态配置\n"
                "4.2 移动端适配：iOS+Android+微信小程序+人脸识别+电子签章+进度推送\n"
                "4.3 流程优化：20+高频办件优化+材料免提交+时限压缩30%+并联审批+好差评\n"
                "4.4 用户体验：智能导办+无障碍适配+多语言+个性化首页\n"
                "需人工确认：流程优化需逐项与业务部门确认。"), needs_review=True),
            SolutionSection(title="5. 数据迁移与兼容方案", content="现有数据完整迁移+迁移过程不影响在线业务+迁移后一致性校验\n需人工确认：迁移方案需根据现有数据量设计。", needs_review=True),
            SolutionSection(title="6. 安全体系设计", content="等保二级+统一认证+电子签章+操作审计"),
            SolutionSection(title="7. 实施计划", content=(
                "项目周期60天：\n"
                "- 第1阶段（1-10天）：需求确认+影响分析+方案设计\n"
                "- 第2阶段（11-35天）：核心功能升级+移动端开发+流程优化\n"
                "- 第3阶段（36-50天）：体验优化+数据迁移+联调测试\n"
                "- 第4阶段（51-60天）：培训+试运行+验收\n"
                "需人工确认：计划需根据现有系统复杂度调整。"), needs_review=True),
            SolutionSection(title="8. 项目团队配置", content="项目经理1人、技术负责人1人、前端3人、后端3人、测试2人\n需人工确认：人员配置需根据企业实际情况调整。", needs_review=True),
            SolutionSection(title="9. 测试验收方案", content="功能回归+移动端兼容性测试+性能测试+用户验收"),
            SolutionSection(title="10. 培训方案", content="培训10天，覆盖管理员、窗口工作人员、审批人员"),
            SolutionSection(title="11. 运维服务方案", content="质保期3年，7x24技术支持，1小时响应，每季度巡检"),
            SolutionSection(title="12. 风险控制方案", content="升级风险：灰度发布+回滚方案\n流程风险：逐项与业务部门确认\n数据风险：迁移前后一致性校验"),
        ]

    async def llm_run(self, context: AgentContext, llm_output: str) -> AgentResult:
        try:
            import re
            # 使用二级标题分割大模型输出的 markdown
            parts = re.split(r'^##\s+(.+)$', llm_output, flags=re.MULTILINE)
            
            sections = []
            # 第一部分是 ## 之前的文字（如前言或导言）
            intro = parts[0].strip()
            if intro:
                sections.append(SolutionSection(
                    title="项目背景与前言",
                    content=intro,
                    needs_review=False
                ))
                
            # 奇数索引为标题，偶数索引为内容
            for i in range(1, len(parts), 2):
                title = parts[i].strip()
                content = parts[i+1].strip() if i+1 < len(parts) else ""
                needs_review = "需人工确认" in content or "人工确认" in content
                
                sections.append(SolutionSection(
                    title=title,
                    content=content,
                    needs_review=needs_review
                ))
                
            if not sections:
                # 尝试用一级标题分割
                parts = re.split(r'^#\s+(.+)$', llm_output, flags=re.MULTILINE)
                for i in range(1, len(parts), 2):
                    title = parts[i].strip()
                    content = parts[i+1].strip() if i+1 < len(parts) else ""
                    needs_review = "需人工确认" in content or "人工确认" in content
                    sections.append(SolutionSection(
                        title=title,
                        content=content,
                        needs_review=needs_review
                    ))
                    
            if not sections:
                # 如果没有找到任何标题，把所有内容当作一个章节
                sections.append(SolutionSection(
                    title="技术方案内容",
                    content=llm_output,
                    needs_review="需人工确认" in llm_output
                ))
                
            solution = SolutionResult()
            solution.sections = sections
            solution.toc = [s.title for s in sections]
            solution.total_words = sum(len(s.content) for s in sections)
            
            return AgentResult(
                agent=self.name,
                output=solution.model_dump(),
                summary=f"生成技术方案初稿（LLM），共{len(solution.sections)}个章节，约{solution.total_words}字",
                references=["LLM生成技术方案"]
            )
        except Exception as e:
            self.logger.warning(f"LLM 技术方案解析失败: {e}，将退回到规则模式提取")
            return await self.mock_run(context)

    def _build_prompt(self, context: AgentContext) -> str:
        return f"""请基于以下招标文件生成技术方案初稿，包含必要的系统架构设计、功能设计、实施计划等章节：

招标文件内容：
{context.tender_text[:3000]}

请使用标准 Markdown 格式编写，每个章节请用 '## ' 作为二级标题开头，以便解析。"""

    def _build_system_prompt(self) -> str:
        return "你是政企软件技术方案撰写专家。请生成技术方案初稿，不确定内容标注'需人工确认'。"
