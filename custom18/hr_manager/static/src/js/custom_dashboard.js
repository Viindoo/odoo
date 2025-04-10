import {Component, useEnv} from "@odoo/owl";
import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";

export class CustomDashboard extends Component{
	setup(){
		this.orm = useService("orm");
		this.action = useService("action");
		this.env = useEnv();
	}
	
	async mounted(){
		const employees = await this.orm.searchRead("company.employee", [],["name","job_title"]);
		console.log("Employees:", employees);

	}
}
CustomDashboard.template = "owl.CustomDashboard";

registry.category("actions").add("custom_dashboard", CustomDashboard);