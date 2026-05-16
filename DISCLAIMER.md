# Disclaimer

**AI Kill Switch Protocol (AKSP)**  
The Faulkner Group | Version 1.0.0

---

## Not a Medical Device

This software is a **reference governance framework and implementation template**. It is not a cleared or approved medical device under FDA 21 CFR Part 820, ISO 13485, or any other medical device regulatory framework. It has not been submitted to or reviewed by the U.S. Food and Drug Administration (FDA), the European Medicines Agency (EMA), or any other regulatory authority.

Do not use this software as a standalone patient safety system in a clinical environment without independent validation, certification, and regulatory review appropriate to your jurisdiction and intended use.

---

## Not Legal or Compliance Advice

The compliance mappings in this repository (HIPAA, FDA 21 CFR Part 11, ISO 13485:2016, ONC HTI-1, The Joint Commission) are provided for **reference and architectural guidance only**. They do not constitute legal advice, regulatory compliance certification, or a guarantee that any system built using this framework will satisfy applicable legal or regulatory requirements.

You are solely responsible for ensuring that any system you build, deploy, or operate using this framework complies with all applicable laws, regulations, and standards in your jurisdiction. Consult qualified legal counsel and compliance professionals before deploying in a regulated healthcare environment.

---

## PHI and HIPAA

This framework is designed with HIPAA-aligned patterns in mind, but **does not by itself make any system HIPAA-compliant**. Organizations deploying systems that touch Protected Health Information (PHI) must conduct their own HIPAA risk analysis, establish appropriate Business Associate Agreements (BAAs), implement required technical safeguards, and validate compliance independently.

The Faulkner Group assumes no liability for PHI exposure, data breaches, or regulatory violations arising from the use of this framework.

---

## No Warranty

This software is provided **"as is"**, without warranty of any kind, express or implied, including but not limited to the warranties of merchantability, fitness for a particular purpose, or non-infringement. In no event shall the authors or The Faulkner Group be liable for any claim, damages, or other liability — including but not limited to patient harm, clinical adverse events, or regulatory penalties — arising from the use of this software.

See the [MIT License](./LICENSE) for the full terms.

---

## Production Deployment

Before deploying any system built on this framework in a production clinical environment, you **must**:

- Conduct an independent security review and penetration test
- Validate all kill switch trigger thresholds for your specific clinical context
- Establish and test escalation paths with your clinical operations team
- Obtain required regulatory clearances for your intended use
- Implement and test disaster recovery and business continuity procedures
- Train all personnel who will operate, override, or reinstate AI systems under this protocol

---

*The Faulkner Group provides healthcare IT architecture advisory services. For production deployment guidance, contact [john@thefaulknergroupadvisors.com](mailto:john@thefaulknergroupadvisors.com).*
